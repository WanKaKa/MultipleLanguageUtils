import os
import re

from multiple_language import kevin_utils
import multiple_language.database

log_delete_res_string = "log_delete_res_string.txt"


def delete_android_values_string(project_res_dir, input_strings,
                                 callback=None, ignore_language_list=None, copy_mode=None):
    if callback:
        callback(1, 100)

    data = {
        'translate_string': input_strings,
        'project_res_dir': project_res_dir
    }
    multiple_language.database.set_json_data(data)

    if not os.path.exists(kevin_utils.get_log_path()):
        os.makedirs(kevin_utils.get_log_path())
    log_file = open(kevin_utils.get_log_path() + log_delete_res_string, mode='w', encoding='utf-8')

    delete_string_key_list = kevin_utils.analysis_equal_string(input_strings, log_file, copy_mode=copy_mode)
    for root, dirs, file_paths in os.walk(project_res_dir):
        if dirs:
            count = 0
            for res_dir in dirs:
                count += 1

                is_pass_path = False
                if ignore_language_list:
                    for ignore_language in ignore_language_list:
                        if ignore_language and ignore_language in res_dir:
                            is_pass_path = True

                if not is_pass_path and os.path.exists(project_res_dir + "\\" + res_dir):
                    if "values" in res_dir:  # res_dir != "values"
                        kevin_utils.print_log(log_file, "\n%s\n" % res_dir)
                        for path in os.listdir(project_res_dir + "\\" + res_dir):
                            file_path = project_res_dir + "\\" + res_dir + "\\" + path
                            if kevin_utils.get_filter_file_name(copy_mode) in file_path and os.path.isfile(file_path):
                                tmp_file_path = file_path + ".ijs"
                                file = open(file_path, mode='r', encoding='utf-8')
                                tmp_file = open(tmp_file_path, mode='w', encoding='utf-8')
                                line = file.readline()
                                temp_read_str = ""
                                while line:
                                    temp_read_str += line
                                    end_string = "</%s>" % kevin_utils.get_filter_key_value(copy_mode)
                                    if "resources" in temp_read_str or end_string in temp_read_str:
                                        key_list = re.findall(
                                            kevin_utils.get_filter_key_regular(copy_mode), temp_read_str)
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
