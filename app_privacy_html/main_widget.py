import os

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget
from app_privacy_html import main_ui

HTML_HEADER = """
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    </head>
    <body>
        <p>
"""

HTML_FOOTER = """
        </p>
    </body>
</html>
"""


class MainWidget(QWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self.ui = main_ui.Ui_Form()
        self.ui.setupUi(self)

        self.setWindowTitle("TXT转HTML")
        self.ui.start.clicked.connect(self.show_time)

    def show_time(self):
        # file_path = analysis_input_path(self.ui.input)
        file_path = "C:\\Work\\ASProjects\\ScreenRecorderTabAS\\app\\src\\main\\assets"
        if os.path.isdir(file_path):
            self.ui.message.setText("文件数 = %d 表演中 玩会手机" % len(os.listdir(file_path)))
            self.txt_to_html(file_path)
        else:
            self.txt_to_html_task(file_path)

    def txt_to_html(self, dir_path):
        file_list = os.listdir(dir_path)
        for file_name in file_list:
            file = os.path.join(dir_path, file_name)
            if os.path.isdir(file):
                self.txt_to_html(file)
            else:
                self.txt_to_html_task(file)
                pass

    def txt_to_html_task(self, file):
        file_name = os.path.basename(file)
        if "AppPrivacy.txt" in file_name or "AppPrivacy_cn.txt" in file_name:
            print(file_name)
            html_file = open(file.replace(".txt", ".html"), mode='w', encoding='utf-8')
            txt_file = open(file, mode='r', encoding='utf-8')

            html_file.write(HTML_HEADER)
            line = txt_file.readline()
            while line:
                html_file.write(line[:-1] + "<br>\n")
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
