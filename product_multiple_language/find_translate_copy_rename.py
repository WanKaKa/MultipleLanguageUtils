import os
import re

from multiple_language import kevin_utils, multiple_language_utils

log_find_translate_copy_rename = "log_find_translate_copy_rename.txt"
filter_string_key_regular = """<string name=".*">(.+?)</string>"""

translate_reference_key_list = []
translate_project_key_list = []


def find_translate(translate_res_dir, project_res_dir):
    global translate_reference_key_list
    translate_reference_key_list = []
    global translate_project_key_list
    translate_project_key_list = []

    log_file = open(kevin_utils.get_log_path() + log_find_translate_copy_rename, mode='w', encoding='utf-8')

    translate_string_list = ""
    for path in kevin_utils.java_string_file_name_list:
        file_path = project_res_dir + "\\values\\" + path

        if os.path.exists(file_path):
            file = open(file_path, encoding='utf-8')
            line = file.readline()
            temp_read_str = ""
            while line:
                temp_read_str += line
                if "resources" in temp_read_str or "</string>" in temp_read_str:
                    string_list = re.findall(filter_string_key_regular, temp_read_str)
                    if string_list:
                        for i in range(len(string_list)):
                            reference_key = judge_translate_exist(log_file, translate_res_dir, string_list[i])
                            if reference_key:
                                translate_reference_key_list.append(reference_key)
                                project_key = re.findall(kevin_utils.filter_string_key_regular, temp_read_str)[i]
                                translate_project_key_list.append(project_key)

                                string = create_sting(project_key, string_list[i])
                                translate_string_list = translate_string_list + string + "\n"

                                kevin_utils.print_log(log_file,
                                                      "竞争产品中Key: %s 项目中Key: %s\n" % (reference_key, project_key))
                                kevin_utils.print_log(log_file, "%s\n" % string)
                        kevin_utils.print_log(log_file, "\n%s\n" % ("*" * 50))
                    temp_read_str = ""
                line = file.readline()
            file.close()
    log_file.close()
    print(translate_reference_key_list)
    print(translate_project_key_list)
    translate_res_delete_string(translate_res_dir)
    translate_res_rename_string(translate_res_dir)
    if translate_string_list:
        multiple_language_utils.copy_multiple_language(translate_string_list, translate_res_dir, project_res_dir)
    return translate_string_list


def create_sting(project_key, translate_string):
    return "<string name=\"" + project_key + "\">" + translate_string + "</string>"


def judge_translate_exist(log_file, translate_res_dir, translate_str):
    kevin_utils.print_log(log_file, "\n项目中的字符: %s\n" % translate_str)
    for path in kevin_utils.java_string_file_name_list:
        file_path = translate_res_dir + "\\values\\" + path

        if os.path.exists(file_path):
            file = open(file_path, encoding='utf-8')
            line = file.readline()
            temp_read_str = ""
            while line:
                temp_read_str += line
                if "resources" in temp_read_str or "</string>" in temp_read_str:
                    string_list = re.findall(filter_string_key_regular, temp_read_str)
                    if string_list:
                        for string in string_list:
                            if string == translate_str:
                                kevin_utils.print_log(log_file, "竞争产品中--存在\n")
                                return re.findall(kevin_utils.filter_string_key_regular, temp_read_str)[0]
                    temp_read_str = ""
                line = file.readline()
            file.close()
    kevin_utils.print_log(log_file, "竞争产品中--不存在\n")
    return ""


def translate_res_delete_string(translate_res_dir):
    for root, dirs, file_paths in os.walk(translate_res_dir):
        if dirs:
            for res_dir_name in dirs:
                for file_name in kevin_utils.java_string_file_name_list:
                    file_path = translate_res_dir + "\\" + res_dir_name + "\\" + file_name
                    if os.path.exists(file_path):
                        file = open(file_path, encoding='utf-8')
                        temp_file = open(file_path + ".ijs", "w", encoding='utf-8')
                        line = file.readline()
                        temp_read_str = ""
                        while line:
                            temp_read_str += line
                            if "resources" in temp_read_str or "</string>" in temp_read_str:
                                key_list = re.findall(kevin_utils.filter_string_key_regular, temp_read_str)
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


def translate_res_rename_string(translate_res_dir):
    for root, dirs, file_paths in os.walk(translate_res_dir):
        if dirs:
            for res_dir_name in dirs:
                for file_name in kevin_utils.java_string_file_name_list:
                    file_path = translate_res_dir + "\\" + res_dir_name + "\\" + file_name
                    if os.path.exists(file_path):
                        file = open(file_path, encoding='utf-8')
                        temp_file = open(file_path + ".ijs", "w", encoding='utf-8')
                        line = file.readline()
                        temp_read_str = ""
                        while line:
                            temp_read_str += line
                            if "resources" in temp_read_str or "</string>" in temp_read_str:
                                key_list = re.findall(kevin_utils.filter_string_key_regular, temp_read_str)
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
