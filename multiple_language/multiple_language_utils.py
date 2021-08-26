import os
import re
from multiple_language import kevin_utils
import multiple_language.database

language_log_name = "log_multiple_language.txt"

# 过滤的文件夹
filter_folder = ["large", "small", "dpi", "land", "port"]

ignore_language_value_list = [
    "values-ar",
    "values-fa",
    "values-he",
    "values-iw",
    "values-ur",
    "values-ug",
    "values-en",
    "values-zh"
]

translate_string = ""
translate_res_dir = ""
project_res_dir = ""


def copy_multiple_language(input1, input2, input3, callback=None, ignore_language_list=None):
    if callback:
        callback(1, 100, label="正在拷贝...")

    if not os.path.exists(kevin_utils.get_log_path()):
        os.makedirs(kevin_utils.get_log_path())
    log_file = open(kevin_utils.get_log_path() + language_log_name, mode='w', encoding='utf-8')

    global translate_string
    translate_string = input1
    # kevin_utils.print_log(log_file, "%s\n" % translate_string)

    global translate_res_dir
    translate_res_dir = input2
    # kevin_utils.print_log(log_file, "%s\n" % translate_res_dir)

    global project_res_dir
    project_res_dir = input3
    # kevin_utils.print_log(log_file, "%s\n" % project_res_dir)

    data = {
        'translate_string': translate_string,
        'translate_res_dir': translate_res_dir,
        'project_res_dir': project_res_dir
    }
    multiple_language.database.set_json_data(data)

    kevin_utils.print_log(log_file, "%s 解析复制开始 %s\n\n" % ("*" * 24, "*" * 24))
    if isinstance(translate_string, list):
        add_string_key_list = translate_string
    else:
        add_string_key_list = kevin_utils.analysis_equal_string(translate_string, log_file)
    if project_res_dir and os.path.exists(project_res_dir):
        for root, dirs, file_paths in os.walk(translate_res_dir):
            if root == translate_res_dir and dirs:
                kevin_utils.print_log(log_file, "\nroot = %s\n" % root)
                kevin_utils.print_log(log_file, "dirs:\n")
                kevin_utils.print_list_log(log_file, dirs, 6, 30)
                kevin_utils.print_log(log_file, "files:\n")
                kevin_utils.print_list_log(log_file, file_paths, 1, 0)
                kevin_utils.print_log(log_file, "\n%s\n" % ("*" * 50))
                count = 0
                for res_dir_name in dirs:
                    count += 1
                    is_pass_path = False
                    if "values" not in res_dir_name:
                        # 文件夹名称不包含values的文件跳过
                        is_pass_path = True
                    else:
                        if ignore_language_list:
                            for ignore_language in ignore_language_list:
                                if ignore_language and ignore_language in res_dir_name:
                                    is_pass_path = True
                        for i in range(9):
                            if str(i) in res_dir_name:
                                # 文件夹名称包含数字0-9的文件跳过
                                is_pass_path = True
                        for str_folder in filter_folder:
                            if str_folder in res_dir_name:
                                # 跳过过滤的文件夹
                                is_pass_path = True
                    if not is_pass_path and res_dir_name != "values":
                        analysis_add_string(res_dir_name, add_string_key_list, log_file)
                    if callback:
                        callback(count, len(dirs))
    kevin_utils.print_log(log_file, "\n%s 解析复制结束 %s\n" % ("*" * 24, "*" * 24))
    log_file.close()
    if callback:
        callback(100, 100)


def analysis_add_string(res_dir_name, add_string_key_list, log_file):
    """
        判断项目资源文件夹中是否存在翻译字符，存在则不添加

        res_dir_name : 资源文件夹名称
        add_string_key_list : 需要添加字符的Key集合
    """
    no_string_or_strings = True
    temp_file_list = os.listdir(translate_res_dir + "\\" + res_dir_name)
    for file_name in temp_file_list:
        file_path = translate_res_dir + "\\" + res_dir_name + "\\" + file_name
        if "string" in file_name and os.path.isfile(file_path):
            add_string = ""
            no_string_or_strings = False
            file = open(file_path, encoding='utf-8')
            line = file.readline()
            temp_read_str = ""
            while line:
                temp_read_str += line
                if "resources" in temp_read_str or "</string>" in temp_read_str:
                    key_list = re.findall(kevin_utils.filter_string_key_regular, temp_read_str)
                    if key_list:
                        for key in add_string_key_list:
                            if key == key_list[0]:
                                if not string_in_project(res_dir_name, key_list[0]) and \
                                        key not in re.findall(kevin_utils.filter_string_key_regular, add_string):
                                    add_string += "\n" if len(add_string) != 0 else ""
                                    if temp_read_str.endswith("\n"):
                                        add_string += temp_read_str[:-1]
                                    else:
                                        add_string += temp_read_str
                                    break
                    temp_read_str = ""
                line = file.readline()
            file.close()

            add_string = add_string[:-1] if add_string.endswith("\n") else add_string
            if add_string:
                # 判断项目是否存在对应的语言文件夹，不存在则创建文件夹和文件
                if not os.path.exists(project_res_dir + "\\" + res_dir_name):
                    os.makedirs(project_res_dir + "\\" + res_dir_name)
                    file = open(project_res_dir + "\\" + res_dir_name + "\\strings.xml", mode='w', encoding='utf-8')
                    file.write("""<?xml version="1.0" encoding="utf-8"?>\n<resources>\n</resources>""")
                    file.close()
                else:
                    temp_list = os.listdir(project_res_dir + "\\" + res_dir_name)
                    if not temp_list or ("strings.xml" not in temp_list and "string.xml" not in temp_list):
                        file = open(project_res_dir + "\\" + res_dir_name + "\\strings.xml", mode='w', encoding='utf-8')
                        file.write("""<?xml version="1.0" encoding="utf-8"?>\n<resources>\n</resources>""")
                        file.close()

                add_string_to_project_res(res_dir_name, add_string)
                kevin_utils.print_log(
                    log_file, "\n语言文件夹 = %s\n新增字符:\n%s\n\n%s\n" % (res_dir_name, add_string, "*" * 50))
            else:
                kevin_utils.print_log(log_file, "\n语言文件夹 = %s\n新增字符:空\n\n%s\n" % (res_dir_name, "*" * 50))
    if no_string_or_strings:
        kevin_utils.print_log(
            log_file, "\n语言文件夹 = %s\n此文件夹下没有string.xml或者strings.xml\n\n%s\n" % (res_dir_name, "*" * 50))


def string_in_project(res_dir_name, string_key):
    """
        判断字符在项目文件中是否不存在

        res_dir_name : 资源文件夹名称
        string_key : 字符名称
    """
    dir_path = project_res_dir + "\\" + res_dir_name + "\\"
    if not os.path.exists(dir_path) or os.path.isfile(dir_path):
        return False
    temp_file_list = os.listdir(dir_path)
    for file_name in temp_file_list:
        file_path = project_res_dir + "\\" + res_dir_name + "\\" + file_name
        if "string" in file_name and os.path.isfile(file_path):
            if os.path.exists(file_path):
                file = open(file_path, encoding='utf-8')
                line = file.readline()
                temp_read_str = ""
                while line:
                    temp_read_str += line
                    if "resources" in temp_read_str or "</string>" in temp_read_str:
                        key_list = re.findall(kevin_utils.filter_string_key_regular, temp_read_str)
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
    for file_name in kevin_utils.java_string_file_name_list:
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
