import getpass
import re

language_log_name = "language_log.txt"

java_string_file_name_list = ["string.xml", "strings.xml"]
filter_string_key_regular = """<string name="(.+?)">"""


def get_log_path():
    return 'C:\\Users\\' + getpass.getuser() + '\\Kevin\\'


def print_log(log_file, log_info):
    print(log_info)
    log_file.write(log_info)


def analysis_equal_string(strings, log_file):
    add_string_key_list = []
    temp_read_str = ""
    for line in strings.split("\n"):
        temp_read_str += line
        if "resources" in temp_read_str or "</string>" in temp_read_str:
            key_list = re.findall(filter_string_key_regular, temp_read_str)
            if key_list:
                add_string_key_list.append(key_list[0])
            temp_read_str = ""
    print_log(log_file, "解析输入的字符的KEY:\n%s\n\n%s\n" % (add_string_key_list, "*" * 50))
    return add_string_key_list
