import os
import re
import sys
from multiple_language import kevin_utils
from multiple_language import multiple_language_utils
from product_multiple_language import main_window
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QDialog, QMessageBox


class MainWindow(QWidget, main_window.Ui_Form):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)


def copy_multiple_language():
    reply = QMessageBox.question(main_window, '拷贝字符', '确认拷贝吗',
                                 QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
    if reply == QMessageBox.Yes:
        main_window.pushButton_2.setText("正在拷贝中，请勿重复点击")
        main_window.pushButton_2.setStyleSheet("background-color: red;\n"
                                               "color: rgb(255, 255, 255);\n"
                                               "font: 12pt \"微软雅黑\";")

        translate_string = main_window.textEdit.toPlainText().strip("\n")
        translate_res_dir = main_window.lineEdit.text().strip("\n")
        project_res_dir = main_window.lineEdit_2.text().strip("\n")
        multiple_language_utils.copy_multiple_language(translate_string, translate_res_dir, project_res_dir)
        main_window.pushButton_2.setText("拷贝")
        main_window.pushButton_2.setStyleSheet("background-color: rgb(0, 170, 255);\n"
                                               "color: rgb(255, 255, 255);\n"
                                               "font: 12pt \"微软雅黑\";")


def delete_android_values_string():
    pass


def print_log(log_file, log_info):
    print(log_info)
    log_file.write(log_info)
    main_window.textBrowser.append(log_info)


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

    main_window.pushButton_2.clicked.connect(copy_multiple_language)
    main_window.pushButton_2.clicked.connect(delete_android_values_string)

    if os.path.exists(kevin_utils.get_log_path() + kevin_utils.language_log_name):
        read_log = open(kevin_utils.get_log_path() + kevin_utils.language_log_name,
                        mode='r', encoding='utf-8')
        line_log = read_log.readline()
        while line_log:
            if (not re.findall(kevin_utils.filter_string_key_regular, line_log)) \
                    and (not re.findall(kevin_utils.filter_explain_string_key_regular, line_log)) \
                    and ("</string>" not in line_log) \
                    and (line_log.replace("\n", "") != "") \
                    and ("\\res" in line_log):
                break
            main_window.textEdit.append(line_log.strip("\n"))
            line_log = read_log.readline()
        main_window.lineEdit.insert(line_log.replace("\n", ""))
        main_window.lineEdit_2.insert(read_log.readline().replace("\n", ""))
        read_log.close()

    kevin_utils.print_log = print_log

    sys.exit(app.exec_())
