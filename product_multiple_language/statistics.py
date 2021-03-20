import os
import re

from multiple_language import kevin_utils


def statistics_string(project_res_dir, text_browser):
    text_browser.clear()
    for path in kevin_utils.java_string_file_name_list:
        file_path = project_res_dir + "\\values\\" + path

        if os.path.exists(file_path):
            file = open(file_path, encoding='utf-8')
            line = file.readline()
            temp_read_str = ""
            while line:
                temp_read_str += line
                if "resources" in temp_read_str or "</string>" in temp_read_str:
                    string_list = re.findall(kevin_utils.filter_string_key_regular, temp_read_str)
                    if string_list:
                        text_browser.append(temp_read_str.strip("\n"))
                        text_browser.append("翻译数 = %d" % statistics_count(project_res_dir, string_list[0]))
                    temp_read_str = ""
                line = file.readline()
            file.close()


def statistics_count(project_res_dir, string_key):
    for root, dirs, file_paths in os.walk(project_res_dir):
        if dirs:
            count = 0
            for res_dir_name in dirs:
                for file_name in kevin_utils.java_string_file_name_list:
                    file_path = project_res_dir + "\\" + res_dir_name + "\\" + file_name
                    if os.path.exists(file_path):
                        file = open(file_path, encoding='utf-8')
                        line = file.readline()
                        temp_read_str = ""
                        while line:
                            temp_read_str += line
                            if "resources" in temp_read_str or "</string>" in temp_read_str:
                                key_list = re.findall(kevin_utils.filter_string_key_regular, temp_read_str)
                                if key_list:
                                    for key in key_list:
                                        if key == string_key:
                                            count += 1
                                temp_read_str = ""
                            line = file.readline()
                        file.close()
            return count
    return 0
