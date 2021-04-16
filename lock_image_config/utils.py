import os
import shutil
import sys


def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def print_log(log_file, log_info):
    print(log_info)
    if log_file:
        log_file.write(log_info + "\n")


def print_list_log(log_file, log_info, str_count, str_length):
    if isinstance(log_info, list) and len(log_info) != 0:
        count = 0
        temp_string = ""
        for add_key in log_info:
            if count >= str_count:
                print_log(log_file, temp_string)
                count = 0
                temp_string = ""
            temp_string += "%s" % (add_key.ljust(str_length))
            count += 1
        if temp_string:
            print_log(log_file, temp_string)


def delete_dir(dir_path):
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        del_list = os.listdir(dir_path)
        for f in del_list:
            file_path = os.path.join(dir_path, f)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
