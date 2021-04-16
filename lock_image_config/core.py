# 服务器壁纸路径
import os
import shutil

from natsort import natsorted, ns
from lock_image_config import utils

FILTER_DIR_LIST = [".git", "skin_thumb", "xml", "version.xml"]

select_service_url = ""
# 需要操作的壁纸类型（即文件夹名称）
modify_image_type_list = []


def run(service_image_path, work_image_path, service_url, log_file=None, callback=None):
    if callback:
        callback(10, 100, label="正在修改壁纸...")

    global select_service_url
    select_service_url = service_url

    # 解析需要操作的壁纸文件夹
    modify_image_type_list.clear()
    for file in natsorted(os.listdir(work_image_path), alg=ns.PATH):
        if os.path.isdir(work_image_path + "/" + file) and file not in FILTER_DIR_LIST:
            modify_image_type_list.append(file)
    utils.print_log(log_file, "操作的壁纸类型列表:")
    utils.print_list_log(log_file, modify_image_type_list, 6, 20)
    count = 1
    for image_type in modify_image_type_list:
        utils.print_log(log_file, "")
        utils.print_log(log_file, "")
        utils.print_log(log_file, "")
        utils.print_log(log_file, "")
        utils.print_log(log_file, "*" * 100)
        utils.print_log(log_file, "操作壁纸类型 : %s" % image_type)
        modify_image(service_image_path, work_image_path, image_type, log_file=log_file)
        utils.print_log(log_file, "*" * 100)
        if callback:
            callback(count, len(modify_image_type_list))
        count += 1


def modify_image(service_image_path, work_image_path, image_type, log_file=None):
    if os.path.exists(work_image_path + "/xml/skin_" + image_type + ".xml"):
        utils.print_log(log_file, "壁纸已经处理过!!!")
        return

    image_dir_path = work_image_path + "/" + image_type + "/"
    image_file_list = []
    for file in natsorted(os.listdir(image_dir_path), alg=ns.PATH):
        if os.path.isfile(image_dir_path + file):
            image_file_list.append(file)

    thumb_dir_path = work_image_path + "/skin_thumb/" + image_type + "/"
    if not os.path.exists(thumb_dir_path):
        utils.print_log(log_file, "缩略图不存在!!!")
        return

    thumb_file_list = []
    for file in natsorted(os.listdir(thumb_dir_path), alg=ns.PATH):
        if os.path.isfile(thumb_dir_path + file):
            thumb_file_list.append(file)

    if len(image_file_list) == 0 or len(image_file_list) != len(thumb_file_list):
        utils.print_log(log_file, "壁纸和缩略图的数量不一致!!!")
        return

    # 工作目录下不存在xml文件夹，则创建
    if not os.path.exists(work_image_path + "/xml/"):
        os.makedirs(work_image_path + "/xml/")
    # 拷贝服务器配置的配置表，不存在时创建文件
    if os.path.exists(service_image_path + "/xml/skin_" + image_type + ".xml"):
        shutil.copy(service_image_path + "/xml/skin_" + image_type + ".xml", work_image_path + "/xml/")
        utils.print_log(log_file, "配置文件已拷贝")

        start_index = len(os.listdir(service_image_path + "/" + image_type + "/")) + 1
        utils.print_log(log_file, "壁纸 Start Index = %d" % start_index)
    else:
        create_empty_xml_file(work_image_path + "/xml/skin_" + image_type + ".xml")
        utils.print_log(log_file, "新增类型，空配置文件已创建")

        start_index = 1
        utils.print_log(log_file, "壁纸 Start Index = %d" % start_index)

    modify_xml(work_image_path, image_type, start_index, len(image_file_list), log_file=log_file)
    modify_image_name(work_image_path, image_type, start_index, image_file_list, log_file=log_file)
    modify_thumb_name(work_image_path, image_type, start_index, thumb_file_list, log_file=log_file)


def create_empty_xml_file(path):
    file = open(path, mode='w', encoding='utf-8')
    file.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>")
    file.write("\n")
    file.write("<skin>")
    file.write("\n")
    file.write("</skin>")
    file.close()


def modify_xml(work_image_path, image_type, start_index, count, log_file=None):
    utils.print_log(log_file, "")
    utils.print_log(log_file, "")
    utils.print_log(log_file, "修改配置文件--开始")
    old_path = work_image_path + "/xml/skin_" + image_type + ".xml"
    old_file = open(old_path, mode='r', encoding='utf-8')
    new_path = work_image_path + "/xml/skin_" + image_type + ".xml.ijs"
    new_file = open(new_path, mode='w', encoding='utf-8')
    line = old_file.readline()
    while line:
        new_file.write(line)
        if line.replace("\n", "") == "<skin>":
            for i in range(count):
                item_string = create_item_xml(image_type, start_index + i)
                new_file.write(item_string)
                new_file.write("\n")
                utils.print_log(log_file, item_string)
        line = old_file.readline()
    old_file.close()
    new_file.close()
    os.remove(old_path)
    os.rename(new_path, old_path)
    utils.print_log(log_file, "修改配置文件--结束")


def create_item_xml(skin_name, index):
    download_url = select_service_url + skin_name + "/" + skin_name + "_" + int2str(index)
    thumb = select_service_url + "skin_thumb/" + skin_name + "/" + skin_name + "_" + int2str(index)
    url = "skin_img/" + skin_name + "/" + skin_name + "_" + int2str(index) + ".ijs"
    item_str = "    <item" + "\n"
    item_str += "        download_url=" + "\"" + download_url + "\"\n"
    item_str += "        from=" + "\"" + "net" + "\"\n"
    item_str += "        id=" + "\"" + str((index - 1)) + "\"\n"
    item_str += "        thumb=" + "\"" + thumb + "\"\n"
    item_str += "        url=" + "\"" + url + "\" />"
    return item_str


def int2str(index):
    if index < 10:
        return "0" + str(index)
    return str(index)


def modify_image_name(work_image_path, image_type, start_index, image_file_list, log_file=None):
    utils.print_log(log_file, "")
    utils.print_log(log_file, "")
    utils.print_log(log_file, "重命名壁纸--开始")

    utils.print_log(log_file, "重命名前的原始壁纸:")
    utils.print_list_log(log_file, image_file_list, 6, 30)

    index = len(image_file_list) - 1
    while index >= 0:
        new_index = start_index + index
        old_file = work_image_path + "/" + image_type + "/" + image_file_list[index]
        new_file = work_image_path + "/" + image_type + "/" + image_type + "_" + int2str(new_index)
        utils.print_log(log_file, "壁纸原路径: %s" % old_file)
        utils.print_log(log_file, "壁纸新路径: %s" % new_file)
        if old_file == new_file:
            utils.print_log(log_file, "壁纸原路径 == 壁纸新路径")
        else:
            if os.path.exists(new_file):
                new_file += ".conflict"
                utils.print_log(log_file, "壁纸新路径已存在 修改为: %s" % new_file)
            os.rename(old_file, new_file)
            utils.print_log(log_file, "壁纸重命名成功")
        index -= 1

    utils.print_log(log_file, "重命名壁纸--结束")


def modify_thumb_name(work_image_path, image_type, start_index, thumb_file_list, log_file=None):
    utils.print_log(log_file, "")
    utils.print_log(log_file, "")
    utils.print_log(log_file, "重命名缩略图--开始")

    utils.print_log(log_file, "重命名前的缩略图:")
    utils.print_list_log(log_file, thumb_file_list, 6, 30)

    index = len(thumb_file_list) - 1
    while index >= 0:
        new_index = start_index + index
        old_file = work_image_path + "/skin_thumb/" + image_type + "/" + thumb_file_list[index]
        new_file = work_image_path + "/skin_thumb/" + image_type + "/" + image_type + "_" + int2str(new_index)
        utils.print_log(log_file, "缩略图原路径: %s" % old_file)
        utils.print_log(log_file, "缩略图新路径: %s" % new_file)
        if old_file == new_file:
            utils.print_log(log_file, "缩略图原路径 == 缩略图新路径")
        else:
            if os.path.exists(new_file):
                new_file += ".conflict"
                utils.print_log(log_file, "缩略图新路径已存在 修改为: %s" % new_file)
            os.rename(old_file, new_file)
            utils.print_log(log_file, "缩略图重命名成功")
        index -= 1

    utils.print_log(log_file, "重命名缩略图--结束")
