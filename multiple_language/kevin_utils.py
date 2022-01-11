import os
import re
import shutil
import sys

from PyQt5.QtWidgets import QCheckBox, QRadioButton


def get_filter_key_regular(copy_mode=None):
    if "dime" == copy_mode:
        return """\\s*<\\s*dimen \\s*name\\s*=\\s*"(.+?)"\\s*>"""
    else:
        return """\\s*<\\s*string \\s*name\\s*=\\s*"(.+?)"\\s*>"""


def get_filter_key_value(copy_mode=None):
    if "dime" == copy_mode:
        return "dimen"
    else:
        return "string"


def get_filter_file_name(copy_mode=None):
    if "dime" == copy_mode:
        return "dime"
    else:
        return "string"


def get_log_path():
    path = 'C:\\IJoySoft\\' + 'Kevin\\'
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def get_res():
    path = 'C:\\IJoySoft\\Kevin\\res\\'
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def print_log(log_file, log_info):
    print(log_info)
    log_file.write(log_info)


def print_list_log(log_file, log_info, str_count, str_length):
    if isinstance(log_info, list) and len(log_info) != 0:
        count = 0
        for add_key in log_info:
            if count >= str_count:
                print_log(log_file, "\n")
                count = 0
            print_log(log_file, "%s" % (add_key.ljust(str_length)))
            count += 1
        print_log(log_file, "\n")


def analysis_equal_string(strings, log_file, copy_mode=None):
    add_string_key_list = []
    temp_read_str = ""
    for line in strings.split("\n"):
        temp_read_str += line
        end_string = "</%s>" % get_filter_key_value(copy_mode)
        if "resources" in temp_read_str or end_string in temp_read_str:
            key_list = re.findall(get_filter_key_regular(copy_mode), temp_read_str)
            if key_list:
                add_string_key_list.append(key_list[0])
            temp_read_str = ""
    print_log(log_file, "解析输入的字符的KEY:\n")
    print_list_log(log_file, add_string_key_list, 3, 60)
    print_log(log_file, "\n%s\n" % ("*" * 50))
    return add_string_key_list


def open_file(file_path):
    os.system(file_path)


def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def copy_res():
    res_list = os.listdir(get_res())
    for item in os.listdir(resource_path("./ico")):
        if item not in res_list:
            shutil.copyfile(resource_path(os.path.join("ico", item)), os.path.join(get_res(), item))


CHECK_BOX_STYLE = """
QCheckBox{
    background-color: rgb(255, 255, 255);
    font: 12pt \"微软雅黑\";
}
QCheckBox::indicator {
    width:25px;
    height:25px;
}
QCheckBox::indicator:unchecked  {
    image: url(C:/IJoySoft/Kevin/res/check_box_unchecked.png);
}
QCheckBox::indicator:unchecked:hover {
    image: url(C:/IJoySoft/Kevin/res/check_box_unchecked_hover.png);
}
QCheckBox::indicator:checked {
    image: url(C:/IJoySoft/Kevin/res/check_box_checked.png);
}
"""


def set_check_box_style(check_box):
    if isinstance(check_box, QCheckBox):
        check_box.setStyleSheet(CHECK_BOX_STYLE)


RADIO_BUTTON_STYLE_RED = """
QRadioButton{
    background-color: rgb(255, 255, 255);
    font: 10pt \"微软雅黑\";
    color: rgb(255, 0, 0);
}
QRadioButton::indicator {
    width:25px;
    height:25px;
}
QRadioButton::indicator:unchecked  {
    image: url(C:/IJoySoft/Kevin/res/radio_button_normal_unchecked.png);
}
QRadioButton::indicator:unchecked:hover {
    image: url(C:/IJoySoft/Kevin/res/radio_button_normal_unchecked_hover.png);
}
QRadioButton::indicator:checked {
    image: url(C:/IJoySoft/Kevin/res/radio_button_normal_checked.png);
}
"""

RADIO_BUTTON_STYLE_BLACK = """
QRadioButton{
    background-color: rgb(255, 255, 255);
    font: 10pt \"微软雅黑\";
    color: rgb(0, 0, 0);
}
QRadioButton::indicator {
    width:25px;
    height:25px;
}
QRadioButton::indicator:unchecked  {
    image: url(C:/IJoySoft/Kevin/res/radio_button_normal_unchecked.png);
}
QRadioButton::indicator:unchecked:hover {
    image: url(C:/IJoySoft/Kevin/res/radio_button_normal_unchecked_hover.png);
}
QRadioButton::indicator:checked {
    image: url(C:/IJoySoft/Kevin/res/radio_button_normal_checked.png);
}
"""


def set_radio_button_style(check_box, error):
    if isinstance(check_box, QRadioButton):
        if error:
            check_box.setStyleSheet(RADIO_BUTTON_STYLE_RED)
        else:
            check_box.setStyleSheet(RADIO_BUTTON_STYLE_BLACK)


def text_style1(string):
    return "<span style=\"color:#4A8FF8; font:24pt;\">%s</span>" % str(string)


def text_style2(string):
    return "<span style=\"color:#ff0000; font:24pt;\">%s</span>" % str(string)
