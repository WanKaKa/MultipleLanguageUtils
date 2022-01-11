import os
import re

from multiple_language import kevin_utils, multiple_language_utils

log_find_translate_copy_rename = "log_find_translate_copy_rename.txt"
filter_string_value_regular = """<string name=".*">(.+?)</string>"""

translate_reference_key_list = []
translate_project_key_list = []


def find_translate(translate_res_dir, project_res_dir, callback=None, ignore_language_list=None, copy_mode=None):
    if callback:
        callback(1, 100, label="正在解析字符...")

    global translate_reference_key_list
    translate_reference_key_list.clear()
    global translate_project_key_list
    translate_project_key_list.clear()

    if not os.path.exists(kevin_utils.get_log_path()):
        os.makedirs(kevin_utils.get_log_path())
    log_file = open(kevin_utils.get_log_path() + log_find_translate_copy_rename, mode='w', encoding='utf-8')

    translate_string_list = ""
    count = 1
    for path in os.listdir(project_res_dir + "\\values"):
        file_path = project_res_dir + "\\values\\" + path

        if kevin_utils.get_filter_file_name(copy_mode) in file_path and os.path.isfile(file_path):
            file = open(file_path, encoding='utf-8')
            line = file.readline()
            temp_read_str = ""
            while line:
                count += 1
                temp_read_str += line
                end_string = "</%s>" % kevin_utils.get_filter_key_value(copy_mode)
                if "resources" in temp_read_str or end_string in temp_read_str:
                    string_list = re.findall(filter_string_value_regular, temp_read_str)
                    if string_list:
                        for i in range(len(string_list)):
                            lookup_key_list = judge_translate_exist(log_file, translate_res_dir, string_list[i])
                            for reference_key in lookup_key_list:
                                if reference_key and reference_key not in translate_reference_key_list:
                                    project_key = re.findall(
                                        kevin_utils.get_filter_key_regular(copy_mode), temp_read_str)[i]
                                    if project_key and project_key not in translate_project_key_list:
                                        translate_reference_key_list.append(reference_key)
                                        translate_project_key_list.append(project_key)

                                        string = create_sting(project_key, string_list[i])
                                        translate_string_list = translate_string_list + string + "\n"

                                        kevin_utils.print_log(log_file, "竞争产品中Key: %s \n" % reference_key)
                                        kevin_utils.print_log(log_file, "项目中Key: %s\n" % project_key)

                                        kevin_utils.print_log(log_file, "%s\n" % string)
                        kevin_utils.print_log(log_file, "\n%s\n" % ("*" * 50))
                    temp_read_str = ""
                if callback:
                    callback(min(count, 90), 100)
                line = file.readline()
            file.close()
    log_file.close()
    if callback:
        callback(100, 100)

    translate_res_delete_string(translate_res_dir, callback=callback)
    translate_res_rename_string(translate_res_dir, callback=callback)

    if translate_string_list:
        multiple_language_utils.copy_multiple_language(
            translate_string_list, translate_res_dir, project_res_dir, callback=callback,
            ignore_language_list=ignore_language_list, copy_mode=copy_mode)
    return translate_string_list


def create_sting(project_key, translate_string):
    return "<string name=\"" + project_key + "\">" + translate_string + "</string>"


def judge_translate_exist(log_file, translate_res_dir, translate_str, copy_mode=None):
    lookup_key_list = []
    kevin_utils.print_log(log_file, "\n项目中的字符: %s\n" % translate_str)
    for path in os.listdir(translate_res_dir + "\\values"):
        file_path = translate_res_dir + "\\values\\" + path

        if kevin_utils.get_filter_file_name(copy_mode) in file_path and os.path.isfile(file_path):
            file = open(file_path, encoding='utf-8')
            line = file.readline()
            temp_read_str = ""
            while line:
                temp_read_str += line
                end_string = "</%s>" % kevin_utils.get_filter_key_value(copy_mode)
                if "resources" in temp_read_str or end_string in temp_read_str:
                    string_list = re.findall(filter_string_value_regular, temp_read_str)
                    if string_list:
                        for string in string_list:
                            if string == translate_str:
                                lookup_key_list.append(
                                    re.findall(kevin_utils.get_filter_key_regular(copy_mode), temp_read_str)[0])
                    temp_read_str = ""
                line = file.readline()
            file.close()
    return lookup_key_list


def translate_res_delete_string(translate_res_dir, callback=None, copy_mode=None):
    if callback:
        callback(1, 100, label="正在删除重复的Key...")
    for root, dirs, file_paths in os.walk(translate_res_dir):
        if dirs:
            count = 0
            for res_dir_name in dirs:
                count += 1
                for file_name in os.listdir(translate_res_dir + "\\" + res_dir_name):
                    file_path = translate_res_dir + "\\" + res_dir_name + "\\" + file_name
                    if kevin_utils.get_filter_file_name(copy_mode) in file_path and os.path.isfile(file_path):
                        file = open(file_path, encoding='utf-8')
                        temp_file = open(file_path + ".ijs", "w", encoding='utf-8')
                        line = file.readline()
                        temp_read_str = ""
                        while line:
                            temp_read_str += line
                            end_string = "</%s>" % kevin_utils.get_filter_key_value(copy_mode)
                            if "resources" in temp_read_str or end_string in temp_read_str:
                                key_list = re.findall(kevin_utils.get_filter_key_regular(copy_mode), temp_read_str)
                                if key_list:
                                    for i in range(len(key_list)):
                                        if key_list[i] in translate_project_key_list:
                                            index = translate_project_key_list.index(key_list[i])
                                            if translate_reference_key_list[index] != translate_project_key_list[index]:
                                                old_str = "<string name=\"" + key_list[i] + "\">"
                                                new_str = "<string name=\"" + "让此字符变的没有作用" + "\">"
                                                temp_read_str = temp_read_str.replace(old_str, new_str)
                                temp_file.write(temp_read_str)
                                temp_read_str = ""
                            line = file.readline()
                        temp_file.write(temp_read_str)
                        temp_file.close()
                        file.close()
                        os.remove(file_path)
                        os.rename(file_path + ".ijs", file_path)
                if callback:
                    callback(count, len(dirs))
    if callback:
        callback(100, 100)


def translate_res_rename_string(translate_res_dir, callback=None, copy_mode=None):
    if callback:
        callback(1, 100, label="正在重命名Key...")
    for root, dirs, file_paths in os.walk(translate_res_dir):
        if dirs:
            count = 0
            for res_dir_name in dirs:
                count += 1
                for file_name in os.listdir(translate_res_dir + "\\" + res_dir_name):
                    file_path = translate_res_dir + "\\" + res_dir_name + "\\" + file_name
                    if kevin_utils.get_filter_file_name(copy_mode) in file_path and os.path.isfile(file_path):
                        file = open(file_path, encoding='utf-8')
                        temp_file = open(file_path + ".ijs", "w", encoding='utf-8')
                        line = file.readline()
                        temp_read_str = ""
                        while line:
                            temp_read_str += line
                            end_string = "</%s>" % kevin_utils.get_filter_key_value(copy_mode)
                            if "resources" in temp_read_str or end_string in temp_read_str:
                                key_list = re.findall(kevin_utils.get_filter_key_regular(copy_mode), temp_read_str)
                                if key_list:
                                    for i in range(len(translate_reference_key_list)):
                                        if translate_reference_key_list[i] in key_list:
                                            old_str = "<string name=\"" + translate_reference_key_list[i] + "\">"
                                            new_str = "<string name=\"" + translate_project_key_list[i] + "\">"
                                            temp_read_str = temp_read_str.replace(old_str, new_str)
                                temp_file.write(temp_read_str)
                                temp_read_str = ""
                            line = file.readline()
                        temp_file.write(temp_read_str)
                        temp_file.close()
                        file.close()
                        os.remove(file_path)
                        os.rename(file_path + ".ijs", file_path)
                if callback:
                    callback(count, len(dirs))
    if callback:
        callback(100, 100)
