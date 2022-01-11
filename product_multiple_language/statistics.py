import os
import re

from multiple_language import kevin_utils

string_key_list = []
string_value_list = []
string_count_list = {}


def statistics_string(project_res_dir, browser=None, copy_mode=None):
    if browser:
        browser.clear()
    string_key_list.clear()
    string_value_list.clear()
    string_count_list.clear()
    for path in os.listdir(project_res_dir + "\\values\\"):
        file_path = project_res_dir + "\\values\\" + path

        if kevin_utils.get_filter_file_name(copy_mode) in file_path and os.path.isfile(file_path):
            file = open(file_path, encoding='utf-8')
            line = file.readline()
            temp_read_str = ""
            while line:
                temp_read_str += line
                end_string = "</%s>" % kevin_utils.get_filter_key_value(copy_mode)
                if "resources" in temp_read_str or end_string in temp_read_str:
                    string_list = re.findall(kevin_utils.get_filter_key_regular(copy_mode), temp_read_str)
                    if string_list:
                        string = temp_read_str.strip("\n").strip(" ")
                        string_key_list.append(string_list[0])
                        string_value_list.append(string)
                        string_count_list[string_list[0]] = 0
                    temp_read_str = ""
                if "<!--" in temp_read_str and "-->" in temp_read_str:
                    if re.findall("""<!--(.+?)-->""", temp_read_str):
                        temp_read_str = ""
                line = file.readline()
            file.close()

            statistics_count(project_res_dir)
            if browser:
                for i in range(len(string_value_list)):
                    browser.append(string_value_list[i])
                    count = string_count_list[string_key_list[i]]
                    if count >= 20:
                        browser.append("翻译数" + kevin_utils.text_style1(count))
                    else:
                        browser.append("翻译数" + kevin_utils.text_style2(count))
                    browser.append("\n")


def statistics_count(project_res_dir, copy_mode=None):
    for root, dirs, file_paths in os.walk(project_res_dir):
        if dirs:
            for res_dir_name in dirs:
                for file_name in os.listdir(project_res_dir + "\\" + res_dir_name):
                    file_path = project_res_dir + "\\" + res_dir_name + "\\" + file_name
                    if kevin_utils.get_filter_file_name(copy_mode) in file_path and os.path.isfile(file_path):
                        file = open(file_path, encoding='utf-8')
                        line = file.readline()
                        temp_read_str = ""
                        while line:
                            temp_read_str += line
                            end_string = "</%s>" % kevin_utils.get_filter_key_value(copy_mode)
                            if "resources" in temp_read_str or end_string in temp_read_str:
                                key_list = re.findall(kevin_utils.get_filter_key_regular(copy_mode), temp_read_str)
                                if key_list:
                                    for key in key_list:
                                        if key in string_key_list:
                                            string_count_list[key] = string_count_list[key] + 1
                                temp_read_str = ""
                            line = file.readline()
                        file.close()
