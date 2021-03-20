import json
import os
import sys
from multiple_language import kevin_utils
from multiple_language import multiple_language_utils
from multiple_language import delete_res_string
from product_multiple_language import main_ui, find_translate_copy_rename, statistics
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QDialog, QMessageBox


class MainWindow(QWidget, main_ui.Ui_Form):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)


def find_translate():
    main_window.pushButton.setText("查重拷贝中，请勿重复点击")
    main_window.pushButton.setStyleSheet(
        "background-color: red;\n""color: rgb(255, 255, 255);\n""font: 10pt \"微软雅黑\";")

    reply = QMessageBox.question(main_window, '拷贝字符', '确认拷贝吗', QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
    if reply == QMessageBox.Yes:
        main_window.textBrowser.clear()
        translate_res_dir = main_window.lineEdit.text().strip("\n")
        project_res_dir = main_window.lineEdit_2.text().strip("\n")
        translate_string_list = find_translate_copy_rename.find_translate(translate_res_dir, project_res_dir)
        if translate_string_list:
            main_window.textEdit.clear()
            main_window.textEdit.append(translate_string_list)
        statistics.statistics_string(project_res_dir, main_window.textBrowser_2)

    main_window.pushButton.setText("查重拷贝")
    main_window.pushButton.setStyleSheet(
        "background-color: rgb(0, 170, 255);\n""color: rgb(255, 255, 255);\n""font: 12pt \"微软雅黑\";")


def copy_multiple_language():
    main_window.pushButton_2.setText("正在拷贝中，请勿重复点击")
    main_window.pushButton_2.setStyleSheet(
        "background-color: red;\n""color: rgb(255, 255, 255);\n""font: 10pt \"微软雅黑\";")

    reply = QMessageBox.question(main_window, '拷贝字符', '确认拷贝吗', QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
    if reply == QMessageBox.Yes:
        main_window.textBrowser.clear()
        translate_string = main_window.textEdit.toPlainText().strip("\n")
        translate_res_dir = main_window.lineEdit.text().strip("\n")
        project_res_dir = main_window.lineEdit_2.text().strip("\n")
        multiple_language_utils.copy_multiple_language(translate_string, translate_res_dir, project_res_dir)
        statistics.statistics_string(project_res_dir, main_window.textBrowser_2)

    main_window.pushButton_2.setText("拷贝")
    main_window.pushButton_2.setStyleSheet(
        "background-color: rgb(0, 170, 255);\n""color: rgb(255, 255, 255);\n""font: 12pt \"微软雅黑\";")


def delete_android_values_string():
    main_window.pushButton_3.setText("正在删除中，请勿重复点击")
    main_window.pushButton_3.setStyleSheet(
        "background-color: red;\n""color: rgb(255, 255, 255);\n""font: 10pt \"微软雅黑\";")

    reply = QMessageBox.question(main_window, '删除字符', '确认删除吗', QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
    if reply == QMessageBox.Yes:
        main_window.textBrowser.clear()
        translate_string = main_window.textEdit.toPlainText().strip("\n")
        project_res_dir = main_window.lineEdit_2.text().strip("\n")
        delete_res_string.delete_android_values_string(project_res_dir, translate_string)
        statistics.statistics_string(project_res_dir, main_window.textBrowser_2)

    main_window.pushButton_3.setText("删除")
    main_window.pushButton_3.setStyleSheet(
        "background-color: rgb(0, 170, 255);\n""color: rgb(255, 255, 255);\n""font: 12pt \"微软雅黑\";")


def print_log(log_file, log_info):
    print(log_info)
    log_file.write(log_info)
    main_window.textBrowser.append(log_info.strip("\n"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    desktop = app.desktop()
    width = desktop.width()
    height = desktop.height()

    main_window = MainWindow()
    main_window.show()
    main_window.move(int((width - 1780) / 2), int((height - 720) / 2))
    main_window.setFixedSize(main_window.width(), main_window.height())
    main_window.setWindowTitle("产品多语言工具-为便捷而生")
    main_window.setWindowIcon(QIcon('favicon.ico'))

    main_window.pushButton.clicked.connect(find_translate)
    main_window.pushButton_2.clicked.connect(copy_multiple_language)
    main_window.pushButton_3.clicked.connect(delete_android_values_string)

    if os.path.exists(kevin_utils.get_log_path() + multiple_language_utils.database_name):
        read_data = open(kevin_utils.get_log_path() + multiple_language_utils.database_name, mode='r', encoding='utf-8')
        data = json.loads(read_data.read())
        if isinstance(data["translate_string"], str):
            main_window.textEdit.append(data["translate_string"])
        if isinstance(data["translate_res_dir"], str):
            main_window.lineEdit.insert(data["translate_res_dir"].replace("\n", ""))
        if isinstance(data["project_res_dir"], str):
            main_window.lineEdit_2.insert(data["project_res_dir"].replace("\n", ""))
        read_data.close()

    kevin_utils.print_log = print_log

    sys.exit(app.exec_())
