import os
import re
from multiple_language.kevin_utils import print_log, filter_string_key_regular, java_string_file_name_list


def delete_empty_res_dir(project_res_dir, log_file):
    for root, dirs, file_paths in os.walk(project_res_dir):
        if dirs:
            for res_dir in dirs:
                is_delete_dir = True
                for child_root, child_dirs, child_file_paths in os.walk(project_res_dir + "\\" + res_dir):
                    if child_dirs:
                        is_delete_dir = False
                    if is_delete_dir:
                        for file_name in child_file_paths:
                            if "string" not in file_name:
                                is_delete_dir = False
                                break
                if is_delete_dir:
                    for path in java_string_file_name_list:
                        file_path = project_res_dir + "\\" + res_dir + "\\" + path
                        if os.path.exists(file_path):
                            file = open(file_path, mode='r', encoding='utf-8')
                            line = file.readline()
                            while line:
                                key_list = re.findall(filter_string_key_regular, line)
                                if key_list:
                                    is_delete_dir = False
                                    break
                                line = file.readline()
                            file.close()
                            if is_delete_dir:
                                os.remove(file_path)
                if is_delete_dir:
                    os.rmdir(project_res_dir + "\\" + res_dir)
                    print_log(log_file, "删除空语言: %s" % res_dir)
