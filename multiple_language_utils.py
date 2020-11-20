import os
import re

java_string_file_name_list = ["string.xml", "strings.xml"]
filter_string_key_regular = """<string name="(.+?)">"""
filter_folder = ["large", "small", "dpi", "land", "port"]


def copy_multiple_language():
    for root, dirs, file_paths in os.walk(translate_res_dir):
        if dirs:
            print("root = %s;\ndirs = %s;\nfiles = %s\n" % (root, dirs, file_paths))
            add_string_key_list = []
            for res_dir_name in dirs:
                isPassPath = False
                if "values" not in res_dir_name:
                    isPassPath = True
                else:
                    for i in range(9):
                        if str(i) in res_dir_name:
                            isPassPath = True
                    for str_folder in filter_folder:
                        if str_folder in res_dir_name:
                            isPassPath = True
                if isPassPath:
                    continue

                if res_dir_name == "values":
                    add_string_key_list = analysis_equal_string(res_dir_name)
                else:
                    analysis_add_string(res_dir_name, add_string_key_list)


def analysis_equal_string(res_dir_name):
    """
        提取相同字符的key值

        res_dir_name : 资源文件夹名称
    """
    for file_name in java_string_file_name_list:
        file_path = translate_res_dir + "\\" + res_dir_name + "\\" + file_name
        add_string_key_list = []
        if os.path.exists(file_path):
            file = open(file_path, encoding='utf-8')
            line = file.readline()
            temp_read_str = ""
            while line:
                temp_read_str += line
                if "resources" in temp_read_str or "</string>" in temp_read_str:
                    key_list = re.findall(filter_string_key_regular, temp_read_str)
                    if key_list:
                        if string_in_project(res_dir_name, key_list[0]):
                            add_string_key_list.append(key_list[0])
                    temp_read_str = ""
                line = file.readline()
            file.close()
            print("新增字符的KEY:\n%s\n%s" % (add_string_key_list, "*" * 50))
            return add_string_key_list


def analysis_add_string(res_dir_name, add_string_key_list):
    """
        判断项目资源文件夹中是否存在翻译字符，存在则不添加

        res_dir_name : 资源文件夹名称
        add_string_key_list : 需要添加字符的Key集合
    """
    for file_name in java_string_file_name_list:
        file_path = translate_res_dir + "\\" + res_dir_name + "\\" + file_name
        add_string = ""
        if os.path.exists(file_path):
            file = open(file_path, encoding='utf-8')
            line = file.readline()
            temp_read_str = ""
            while line:
                temp_read_str += line
                if "resources" in temp_read_str or "</string>" in temp_read_str:
                    key_list = re.findall(filter_string_key_regular, temp_read_str)
                    if key_list:
                        for key in add_string_key_list:
                            if key == key_list[0]:
                                if not string_in_project(res_dir_name, key_list[0]):
                                    add_string = add_string + "\n" + temp_read_str.strip("\n")
                                    break
                    temp_read_str = ""
                line = file.readline()
            file.close()

            add_string = add_string.strip("\n")
            if add_string:
                # 判断项目是否存在对应的语音文件夹，不存在则创建文件夹和文件
                if not os.path.exists(project_res_dir + "\\" + res_dir_name):
                    os.makedirs(project_res_dir + "\\" + res_dir_name)
                    file = open(project_res_dir + "\\" + res_dir_name + "\\strings.xml", mode='w', encoding='utf-8')
                    file.write("""<?xml version="1.0" encoding="utf-8"?>\n<resources>\n</resources>""")
                    file.close()

                add_string_to_project_res(res_dir_name, add_string)
                print("语言文件夹 = %s\n新增字符:\n%s\n%s" % (res_dir_name, add_string, "*" * 50))
            return
    print("语言文件夹 = %s\n此文件夹下没有string.xml或者strings.xml\n%s" % (res_dir_name, "*" * 50))


def string_in_project(res_dir_name, string_key):
    """
        判断字符在项目文件中是否不存在

        res_dir_name : 资源文件夹名称
        string_key : 字符名称
    """
    for file_name in java_string_file_name_list:
        file_path = project_res_dir + "\\" + res_dir_name + "\\" + file_name
        if os.path.exists(file_path):
            file = open(file_path, encoding='utf-8')
            line = file.readline()
            temp_read_str = ""
            while line:
                temp_read_str += line
                if "resources" in temp_read_str or "</string>" in temp_read_str:
                    key_list = re.findall(filter_string_key_regular, temp_read_str)
                    if key_list:
                        if key_list[0] == string_key:
                            return True
                    temp_read_str = ""
                line = file.readline()
            file.close()
    return False


def add_string_to_project_res(res_dir_name, add_str):
    """
        写入新增字符到项目字符文件中

        res_dir_name : 资源文件夹名称
        add_str : 需要插入的字符串
    """
    for file_name in java_string_file_name_list:
        file_path = project_res_dir + "\\" + res_dir_name + "\\" + file_name
        if os.path.exists(file_path):
            tmp_file_path = file_path + ".ijs"
            file = open(file_path, mode='r', encoding='utf-8')
            tmp_file = open(tmp_file_path, mode='w', encoding='utf-8')
            line = file.readline()
            while line:
                if "</resources>" in line:
                    break
                tmp_file.write(line)
                line = file.readline()
            tmp_file.write(add_str)
            tmp_file.write("\n</resources>")
            file.close()
            tmp_file.close()
            os.remove(file_path)
            os.rename(tmp_file_path, file_path)
            break


if __name__ == '__main__':
    print("""
        先把需要翻译的字符手动拷贝到项目的values下

        此脚本的逻辑是
        1. 找到项目中values和翻译文件夹中values相同的字符
        2. 拷贝1步骤中筛选出来的字符到对应的语言目录下，如果项目中对应的语言存在此字符，则跳过拷贝
    """)
    translate_res_dir = input("翻译资源文件夹路径: ")
    project_res_dir = input("项目资源文件夹路径: ")
    print("\n%s 解析复制开始 %s\n" % ("*" * 24, "*" * 24))
    copy_multiple_language()
    print("\n%s 解析复制结束 %s\n" % ("*" * 24, "*" * 24))
    os.system("pause")
