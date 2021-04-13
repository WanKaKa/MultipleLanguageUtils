import os
import re
from multiple_language import kevin_utils

log_delete_res_string = "log_delete_res_string.txt"


def delete_android_values_string(project_res_dir, input_strings, callback=None):
    if callback:
        callback(1, 100)

    if not os.path.exists(kevin_utils.get_log_path()):
        os.makedirs(kevin_utils.get_log_path())
    log_file = open(kevin_utils.get_log_path() + log_delete_res_string, mode='w', encoding='utf-8')

    delete_string_key_list = kevin_utils.analysis_equal_string(input_strings, log_file)
    for root, dirs, file_paths in os.walk(project_res_dir):
        if dirs:
            count = 0
            for res_dir in dirs:
                count += 1
                if os.path.exists(project_res_dir + "\\" + res_dir):
                    if res_dir != "values" and "values" in res_dir:
                        kevin_utils.print_log(log_file, "\n%s\n" % res_dir)
                        for path in kevin_utils.java_string_file_name_list:
                            file_path = project_res_dir + "\\" + res_dir + "\\" + path
                            if os.path.exists(file_path):
                                tmp_file_path = file_path + ".ijs"
                                file = open(file_path, mode='r', encoding='utf-8')
                                tmp_file = open(tmp_file_path, mode='w', encoding='utf-8')
                                line = file.readline()
                                temp_read_str = ""
                                while line:
                                    temp_read_str += line
                                    if "resources" in temp_read_str or "</string>" in temp_read_str:
                                        key_list = re.findall(kevin_utils.filter_string_key_regular, temp_read_str)
                                        delete_enable = False
                                        if key_list:
                                            for key in delete_string_key_list:
                                                if key == key_list[0]:
                                                    delete_enable = True
                                                    kevin_utils.print_log(log_file, "已删除 %s\n" % key)
                                                    break
                                        if not delete_enable:
                                            tmp_file.write(temp_read_str)
                                        temp_read_str = ""
                                    line = file.readline()
                                file.close()
                                tmp_file.close()
                                os.remove(file_path)
                                os.rename(tmp_file_path, file_path)
                                break
                        kevin_utils.print_log(log_file, "\n%s\n" % ("*" * 50))
                if callback:
                    callback(count, len(dirs))
    log_file.close()
    if callback:
        callback(100, 100)
