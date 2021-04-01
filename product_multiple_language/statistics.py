import os
import re

from multiple_language import kevin_utils

string_key_list = []
string_value_list = []
string_count_list = {}


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
                        string = temp_read_str.strip("\n").strip(" ")
                        string_key_list.append(string_list[0])
                        string_value_list.append(string)
                        string_count_list[string] = 0
                    temp_read_str = ""
                if "<!--" in temp_read_str and "-->" in temp_read_str:
                    if re.findall("""<!--(.+?)-->""", temp_read_str):
                        temp_read_str = ""
                line = file.readline()
            file.close()

            statistics_count(project_res_dir)
            for string in string_value_list:
                text_browser.append(string)
                count = string_count_list[string]
                if count >= 20:
                    text_browser.append("翻译数" + kevin_utils.text_style1(count))
                else:
                    text_browser.append("翻译数" + kevin_utils.text_style2(count))
                text_browser.append("\n")


def statistics_count(project_res_dir):
    for root, dirs, file_paths in os.walk(project_res_dir):
        if dirs:
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
                                        if key in string_key_list:
                                            index = string_key_list.index(key)
                                            value = string_value_list[index]
                                            string_count_list[value] = string_count_list[value] + 1
                                temp_read_str = ""
                            line = file.readline()
                        file.close()
