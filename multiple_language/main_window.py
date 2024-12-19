import os
import sys

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QProgressDialog

import multiple_language.database
from multiple_language import main_ui
from multiple_language import kevin_utils
from multiple_language import multiple_language_utils
from multiple_language import delete_res_string


class MainWindow(QWidget, main_ui.Ui_Form):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        kevin_utils.set_radio_button_style(self.copy_string_mode, False)
        kevin_utils.set_radio_button_style(self.copy_dime_mode, False)

        self.copy_string_mode.setChecked(True)


class MainWindowFactory:
    def __init__(self, main_window: MainWindow):
        self.main_window = main_window
        self.ignore_language_button_change_enable = True
        self.ignore_language_text_change_enable = True

        self.progress_dialog = QProgressDialog(self.main_window)
        self.progress_dialog.setMinimumDuration(5)
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.setRange(0, 100)
        self.progress_dialog.setValue(100)

        self.main_window.input_string.insertFromMimeData = self.__insert_from_mime_data
        self.ignore_language_radio_button_list = [
            self.main_window.ignore_language_01,
            self.main_window.ignore_language_02,
            self.main_window.ignore_language_03,
            self.main_window.ignore_language_04,
            self.main_window.ignore_language_05,
            self.main_window.ignore_language_11,
            self.main_window.ignore_language_12,
            self.main_window.ignore_language_13,
            self.main_window.ignore_language_14,
            self.main_window.ignore_language_15
        ]

        data = multiple_language.database.get_json_data()
        _translate = QtCore.QCoreApplication.translate
        if data and "ignore_language_str" in data:
            ignore_language_str = data["ignore_language_str"]
            for i in range(len(multiple_language_utils.ignore_language_value_list)):
                kevin_utils.set_check_box_style(self.ignore_language_radio_button_list[i])
                language_text = multiple_language_utils.ignore_language_value_list[i]
                self.ignore_language_radio_button_list[i].setText(_translate("Form", language_text))
                self.ignore_language_radio_button_list[i].setChecked(language_text in ignore_language_str)
                self.ignore_language_radio_button_list[i].toggled.connect(self.__add_ignore_language)
            self.main_window.ignore_language_text.setText(ignore_language_str)
        else:
            for i in range(len(multiple_language_utils.ignore_language_value_list)):
                kevin_utils.set_check_box_style(self.ignore_language_radio_button_list[i])
                language_text = multiple_language_utils.ignore_language_value_list[i]
                self.ignore_language_radio_button_list[i].setText(_translate("Form", language_text))
                self.ignore_language_radio_button_list[i].setChecked(True)
                if not self.main_window.ignore_language_text.toPlainText():
                    self.main_window.ignore_language_text.setText(language_text)
                else:
                    self.main_window.ignore_language_text.setText(
                        self.main_window.ignore_language_text.toPlainText() + "/" + language_text)
                self.ignore_language_radio_button_list[i].toggled.connect(self.__add_ignore_language)
        self.main_window.ignore_language_text.textChanged.connect(self.__on_ignore_language_text_change)

        # 隐藏多出来的按钮
        if len(self.ignore_language_radio_button_list) > len(multiple_language_utils.ignore_language_value_list):
            for i in range(len(self.ignore_language_radio_button_list)):
                if i >= len(multiple_language_utils.ignore_language_value_list):
                    self.ignore_language_radio_button_list[i].hide()
        self.main_window.ignore_language_select_all.clicked.connect(self.__select_all_ignore_language)

        self.main_window.copy_translate_path.clicked.connect(
            lambda: self.main_window.input_translate_path.setText(self.main_window.old_translate_path.text()))
        self.main_window.copy_project_path.clicked.connect(
            lambda: self.main_window.input_project_path.setText(self.main_window.old_project_path.text()))

        self.main_window.copy_string.clicked.connect(self.copy_multiple_language)
        self.main_window.delete_string.clicked.connect(self.delete_android_values_string)
        self.main_window.open_copy_logo.clicked.connect(lambda: kevin_utils.open_file(
            kevin_utils.get_log_path() + multiple_language_utils.language_log_name))
        self.main_window.open_delete_log.clicked.connect(lambda: kevin_utils.open_file(
            kevin_utils.get_log_path() + delete_res_string.log_delete_res_string))

        if data:
            if "translate_string" in data:
                self.main_window.input_string.setText(data["translate_string"])
            if "translate_res_dir" in data:
                self.main_window.old_translate_path.setText(data["translate_res_dir"].replace("\n", ""))
            if not self.main_window.old_translate_path.text():
                self.main_window.copy_translate_path.hide()
            if "project_res_dir" in data:
                self.main_window.old_project_path.setText(data["project_res_dir"].replace("\n", ""))
            if not self.main_window.old_project_path.text():
                self.main_window.copy_project_path.hide()

    def __add_ignore_language(self):
        if self.ignore_language_button_change_enable:
            self.ignore_language_text_change_enable = False
            self.__set_ignore_language_text()
            self.ignore_language_text_change_enable = True

    def __set_ignore_language_text(self):
        ignore_language_str = self.main_window.ignore_language_text.toPlainText()
        for radio_button in self.ignore_language_radio_button_list:
            if radio_button.isHidden():
                continue
            radio_button_text = radio_button.text()
            if radio_button.isChecked():
                if not ignore_language_str or radio_button_text not in ignore_language_str:
                    ignore_language_str += (radio_button_text + "/")
            else:
                if ignore_language_str and radio_button_text in ignore_language_str:
                    ignore_language_str = ignore_language_str.replace(radio_button_text, "")
        self.main_window.ignore_language_text.setText(ignore_language_str)

    def __select_all_ignore_language(self):
        self.ignore_language_text_change_enable = False
        self.ignore_language_button_change_enable = False

        select_all_enable = False
        for radio_button in self.ignore_language_radio_button_list:
            if radio_button.isHidden():
                continue
            if not radio_button.isChecked():
                select_all_enable = True
        for radio_button in self.ignore_language_radio_button_list:
            if radio_button.isHidden():
                continue
            radio_button.setChecked(select_all_enable)
        self.__set_ignore_language_text()

        self.ignore_language_text_change_enable = True
        self.ignore_language_button_change_enable = True

    def __insert_from_mime_data(self, soc):
        if soc.hasText():
            # 去除粘贴格式
            self.main_window.input_string.textCursor().insertText(soc.text())

    def __on_ignore_language_text_change(self):
        self.ignore_language_button_change_enable = False
        if self.ignore_language_text_change_enable:
            ignore_language_str = self.main_window.ignore_language_text.toPlainText()
            for radio_button in self.ignore_language_radio_button_list:
                if radio_button.isHidden():
                    continue
                radio_button_text = radio_button.text()
                if radio_button_text and radio_button_text in ignore_language_str:
                    radio_button.setChecked(True)
                else:
                    radio_button.setChecked(False)
        self.ignore_language_button_change_enable = True

    def copy_multiple_language(self):
        reply = QMessageBox.question(
            self.main_window, '拷贝', '确定拷贝吗?', QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            input_strings = self.main_window.input_string.toPlainText().strip("\n")
            translate_dir = self.main_window.input_translate_path.toPlainText().strip("\n")
            if translate_dir.startswith("file:///"):
                translate_dir = translate_dir[len("file:///"):]
            project_dir = self.main_window.input_project_path.toPlainText().strip("\n")
            if project_dir.startswith("file:///"):
                project_dir = project_dir[len("file:///"):]
            try:
                self.progress_dialog.setWindowTitle("拷贝")
                self.progress_dialog.setLabelText("正在拷贝...")
                self.progress_dialog.setCancelButtonText("取消")
            except Exception as e:
                print(e)
            value = self.main_window.ignore_language_text.toPlainText()
            multiple_language_utils.copy_multiple_language(
                input_strings, translate_dir, project_dir, callback=self.progress_callback,
                ignore_language_list=value.split("/") if value else None, copy_mode=self.get_copy_mode())

    def delete_android_values_string(self):
        reply = QMessageBox.question(
            self.main_window, '删除', '确定删除吗?', QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            input_strings = self.main_window.input_string.toPlainText().strip("\n")
            project_dir = self.main_window.input_project_path.toPlainText().strip("\n")
            if project_dir.startswith("file:///"):
                project_dir = project_dir[len("file:///"):]
            try:
                self.progress_dialog.setWindowTitle("删除")
                self.progress_dialog.setLabelText("正在删除...")
                self.progress_dialog.setCancelButtonText("取消")
            except Exception as e:
                print(e)
            value = self.main_window.ignore_language_text.toPlainText()
            delete_res_string.delete_android_values_string(
                project_dir, input_strings, callback=self.progress_callback,
                ignore_language_list=value.split("/") if value else None, copy_mode=self.get_copy_mode())

    def progress_callback(self, *args, **kwargs):
        if kwargs and "label" in kwargs:
            self.progress_dialog.setLabelText(kwargs["label"])
        if self.progress_dialog and isinstance(self.progress_dialog, QProgressDialog):
            self.progress_dialog.setValue(int(args[0] / args[1] * 100))

    def get_copy_mode(self):
        if self.main_window.copy_string_mode.isChecked():
            return "string"
        elif self.main_window.copy_dime_mode.isChecked():
            return "dime"


if __name__ == '__main__':
    app = QApplication(sys.argv)
    desktop = app.desktop()
    width = desktop.width()
    height = desktop.height()
    kevin_utils.copy_res()

    window = MainWindow()
    x = int((width - window.frameGeometry().width()) / 2)
    y = int((height - window.frameGeometry().height()) / 2)
    window.move(x, y)
    window.show()
    window.setWindowTitle("翻译拷贝程序-为便捷而生")

    icon_name = kevin_utils.resource_path(os.path.join("ico", "logo_multiple_language.ico"))
    icon = QIcon()
    icon.addPixmap(QPixmap(icon_name))
    window.setWindowIcon(icon)

    MainWindowFactory(window)

    sys.exit(app.exec_())
