import os

import chardet
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget
from app_privacy_html import main_ui

HTML_HEADER = """<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    </head>
    <body>
        <span style="white-space:pre-line;">"""

HTML_FOOTER = """
        </span>
    </body>
</html>"""


class MainWidget(QWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self.ui = main_ui.Ui_Form()
        self.ui.setupUi(self)

        self.setWindowTitle("TXT转HTML")
        self.ui.start.clicked.connect(self.show_time)

    def show_time(self):
        file_path = analysis_input_path(self.ui.input)
        # file_path = "C:\\Work\\ASProjects\\ScreenRecorderTabAS\\app\\src\\main\\assets"
        if os.path.isdir(file_path):
            self.ui.message.setText("数量 = %d 表演中 玩会手机" % len(os.listdir(file_path)))
            self.txt_to_html(file_path)
        else:
            txt_to_html_task(file_path)
        self.ui.message.setText("表演结束")

    def txt_to_html(self, dir_path):
        file_list = os.listdir(dir_path)
        for file_name in file_list:
            file = os.path.join(dir_path, file_name)
            if os.path.isdir(file):
                self.txt_to_html(file)
            else:
                txt_to_html_task(file)
                pass


def txt_to_html_task(file):
    file_name = os.path.basename(file)
    if "AppPrivacy.txt" in file_name or "AppPrivacy_cn.txt" in file_name:
        print(file_name)

        # 根据二进制信息判断编码{'encoding': 'ascii', 'confidence': 1.0, 'language': ''}
        encoding_file = open(file, 'rb')
        encoding_message = chardet.detect(encoding_file.read())
        encoding_file.close()
        print("文件编码格式 = %s" % encoding_message['encoding'])

        html_file = open(file.replace(".txt", ".html"), mode='w', encoding=encoding_message['encoding'])
        txt_file = open(file, mode='r', encoding=encoding_message['encoding'])

        html_file.write(HTML_HEADER)
        line = txt_file.readline()
        while line:
            html_file.write(line.replace("；", "; ")
                            .replace("（", " (")
                            .replace("）", ") ")
                            .replace("：", ": ")
                            .replace("，", ", ")
                            .replace("“", " \"")
                            .replace("”", "\" ")
                            .replace("。", ". ")
                            .replace(") .", ").")
                            .replace("\" )", "\")")
                            .replace("( \"", "(\"")
                            .replace(";  (", "; (")
                            .replace(";   (", "; (")
                            .replace("\" .", "\"."))
            line = txt_file.readline()
        html_file.write(HTML_FOOTER)

        txt_file.close()
        html_file.close()


def analysis_input_path(text_edit):
    input_path = ""
    if isinstance(text_edit, QtWidgets.QTextEdit):
        input_path = text_edit.toPlainText().strip("\n")
    if isinstance(text_edit, QtWidgets.QLineEdit):
        input_path = text_edit.text().strip("\n")
    if input_path.startswith("file:///"):
        return input_path[len("file:///"):]
    return input_path
