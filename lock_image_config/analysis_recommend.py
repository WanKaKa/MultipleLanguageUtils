import os
import shutil

from natsort import natsorted, ns
import cv2
import numpy as np

from lock_image_config import utils
from lock_image_config import core

recommend_image_list = []


def run(service_image_path, work_image_path, recommend_image_path, log_file=None, callback=None):
    callback(10, 100, label="正在分析推荐壁纸...") if callback else ""

    if not os.path.exists(work_image_path + "/xml/") or len(os.listdir(work_image_path + "/xml/")) == 0:
        utils.print_log(log_file, "壁纸还没有处理!!!")
        utils.print_log(log_file, "")
        callback(100, 100) if callback else ""
        return

    if os.path.exists(work_image_path + "/xml/skin_recommend.xml"):
        utils.print_log(log_file, "推荐壁纸已经处理过!!!")
        utils.print_log(log_file, "")
        callback(100, 100) if callback else ""
        return

    if os.path.exists(service_image_path + "/xml/skin_recommend.xml"):
        shutil.copy(service_image_path + "/xml/skin_recommend.xml", work_image_path + "/xml/")
        utils.print_log(log_file, "推荐壁纸配置文件已拷贝")
        utils.print_log(log_file, "")
    else:
        create_empty_xml_file(work_image_path + "/xml/skin_recommend.xml")
        utils.print_log(log_file, "推荐壁纸空配置文件已创建")
        utils.print_log(log_file, "")

    recommend_image_list.clear()
    for file in natsorted(os.listdir(recommend_image_path), alg=ns.PATH):
        if os.path.isfile(recommend_image_path + "/" + file):
            recommend_image_list.append(file)

    utils.print_log(log_file, "操作的推荐壁纸列表:")
    utils.print_list_log(log_file, recommend_image_list, 4, 30)
    utils.print_log(log_file, "")

    all_image_path_list = core.get_all_image(work_image_path)
    utils.print_log(log_file, "所有壁纸壁纸路径列表:")
    utils.print_list_log(log_file, all_image_path_list, 1, 0)

    add_recommend_image_name_list = []
    count = 1
    all_count = len(recommend_image_list) * len(all_image_path_list)
    for file_name in recommend_image_list:
        utils.print_log(log_file, "")
        utils.print_log(log_file, "")
        utils.print_log(log_file, "*" * 100)

        recommend_image_im_read = cv2.imread(recommend_image_path + "/" + file_name)
        recommend_image_a_hash = a_hash(recommend_image_im_read)
        recommend_image_d_hash = d_hash(recommend_image_im_read)
        recommend_image_p_hash = p_hash(recommend_image_im_read)

        similar_value = {}
        for image_path in all_image_path_list:
            # utils.print_log(log_file, "推荐壁纸:%s" % (recommend_image_path + "/" + file_name))
            # utils.print_log(log_file, "原始壁纸:%s" % image_path)

            image_im_read = cv2.imread(image_path)
            image_a_hash = a_hash(image_im_read)
            image_d_hash = d_hash(image_im_read)
            image_p_hash = p_hash(image_im_read)

            value1 = cmp_hash(recommend_image_a_hash, image_a_hash)
            # utils.print_log(log_file, '均值哈希算法相似度: %d' % value1)

            value2 = cmp_hash(recommend_image_d_hash, image_d_hash)
            # utils.print_log(log_file, '差值哈希算法相似度: %d' % value2)

            value3 = cmp_hash(recommend_image_p_hash, image_p_hash)
            # utils.print_log(log_file, '感知哈希算法相似度: %d' % value3)

            value4 = classify_hist_with_split(recommend_image_im_read, image_im_read)
            # utils.print_log(log_file, '三直方图算法相似度: %f' % value4)
            # utils.print_log(log_file, '')

            if len(similar_value) == 0:
                similar_value["image_path"] = image_path
                similar_value["value1"] = value1
                similar_value["value2"] = value2
                similar_value["value3"] = value3
                similar_value["value4"] = value4
            else:
                similar_count = 0
                if value1 < similar_value["value1"]:
                    similar_count += 1
                if value2 < similar_value["value2"]:
                    similar_count += 1
                if value3 < similar_value["value3"]:
                    similar_count += 1
                if value4 > similar_value["value4"]:
                    similar_count += 1
                if similar_count >= 3:
                    similar_value["image_path"] = image_path
                    similar_value["value1"] = value1
                    similar_value["value2"] = value2
                    similar_value["value3"] = value3
                    similar_value["value4"] = value4

            callback(count, all_count) if callback else ""
            count += 1
        add_recommend_image_name_list.append(os.path.basename(similar_value["image_path"]))
        utils.print_log(log_file, "相似度最大的壁纸")
        utils.print_log(log_file, "推荐壁纸:%s" % (recommend_image_path + "/" + file_name))
        utils.print_log(log_file, "原始壁纸:%s" % similar_value["image_path"])
        utils.print_log(log_file, '均值哈希算法相似度: %d' % similar_value["value1"])
        utils.print_log(log_file, '差值哈希算法相似度: %d' % similar_value["value2"])
        utils.print_log(log_file, '感知哈希算法相似度: %d' % similar_value["value3"])
        utils.print_log(log_file, '三直方图算法相似度: %f' % similar_value["value4"])
        utils.print_log(log_file, "*" * 100)
    modify_recommend_xml(work_image_path, add_recommend_image_name_list, log_file=log_file)


def create_empty_xml_file(path):
    file = open(path, mode='w', encoding='utf-8')
    file.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>")
    file.write("\n")
    file.write("<skin>")
    file.write("\n")
    file.write("</skin>")
    file.close()


def modify_recommend_xml(work_image_path, add_recommend_image_name_list, log_file=None):
    utils.print_log(log_file, "")
    utils.print_log(log_file, "")
    utils.print_log(log_file, "*" * 100)
    utils.print_log(log_file, "修改推荐配置文件--开始")

    old_path = work_image_path + "/xml/skin_recommend.xml"
    old_file = open(old_path, mode='r', encoding='utf-8')
    new_path = work_image_path + "/xml/skin_recommend.xml.ijs"
    new_file = open(new_path, mode='w', encoding='utf-8')
    line = old_file.readline()
    while line:
        new_file.write(line)
        if line.replace("\n", "") == "<skin>":
            for name in add_recommend_image_name_list:
                image_type = str(name).split("_")[0]
                index = int(name.split("_")[1]) if "." not in name else int(name.split("_")[1].split(".")[0])
                item_string = core.create_item_xml(image_type, index)
                new_file.write(item_string)
                new_file.write("\n")
                utils.print_log(log_file, item_string)
        line = old_file.readline()
    old_file.close()
    new_file.close()
    os.remove(old_path)
    os.rename(new_path, old_path)
    utils.print_log(log_file, "修改推荐配置文件--结束")
    utils.print_log(log_file, "*" * 100)


# 均值哈希算法
def a_hash(img):
    # 缩放为8*8
    img = cv2.resize(img, (8, 8))
    # 转换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # s为像素和初值为0，hash_str为hash值初值为''
    s = 0
    hash_str = ''
    # 遍历累加求像素和
    for i in range(8):
        for j in range(8):
            s = s + gray[i, j]
    # 求平均灰度
    avg = s / 64
    # 灰度大于平均值为1相反为0生成图片的hash值
    for i in range(8):
        for j in range(8):
            if gray[i, j] > avg:
                hash_str = hash_str + '1'
            else:
                hash_str = hash_str + '0'
    return hash_str


# 差值感知算法
def d_hash(img):
    # 缩放8*8
    img = cv2.resize(img, (9, 8))
    # 转换灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hash_str = ''
    # 每行前一个像素大于后一个像素为1，相反为0，生成哈希
    for i in range(8):
        for j in range(8):
            if gray[i, j] > gray[i, j + 1]:
                hash_str = hash_str + '1'
            else:
                hash_str = hash_str + '0'
    return hash_str


# 感知哈希算法(pHash)
def p_hash(img):
    # 缩放32*32
    img = cv2.resize(img, (32, 32))  # , interpolation=cv2.INTER_CUBIC

    # 转换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 将灰度图转为浮点型，再进行dct变换
    dct = cv2.dct(np.float32(gray))
    # opencv实现的掩码操作
    dct_roi = dct[0:8, 0:8]

    hash_list = []
    acreage = np.mean(dct_roi)
    for i in range(dct_roi.shape[0]):
        for j in range(dct_roi.shape[1]):
            if dct_roi[i, j] > acreage:
                hash_list.append(1)
            else:
                hash_list.append(0)
    return hash_list


# 通过得到RGB每个通道的直方图来计算相似度
def classify_hist_with_split(image1, image2, size=(256, 256)):
    # 将图像resize后，分离为RGB三个通道，再计算每个通道的相似值
    image1 = cv2.resize(image1, size)
    image2 = cv2.resize(image2, size)
    sub_image1 = cv2.split(image1)
    sub_image2 = cv2.split(image2)
    sub_data = 0
    for im1, im2 in zip(sub_image1, sub_image2):
        sub_data += calculate(im1, im2)
    sub_data = sub_data / 3
    return sub_data


# 计算单通道的直方图的相似值
def calculate(image1, image2):
    hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
    hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])
    # 计算直方图的重合度
    degree = 0
    for i in range(len(hist1)):
        if hist1[i] != hist2[i]:
            degree = degree + (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
        else:
            degree = degree + 1
    degree = degree / len(hist1)
    return degree


# Hash值对比
def cmp_hash(hash1, hash2):
    n = 0
    # hash长度不同则返回-1代表传参出错
    if len(hash1) != len(hash2):
        return -1
    # 遍历判断
    for i in range(len(hash1)):
        # 不相等则n计数+1，n最终为相似度
        if hash1[i] != hash2[i]:
            n = n + 1
    return n
