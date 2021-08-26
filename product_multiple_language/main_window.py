import os
import sys

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import Qt

import multiple_language.main_window
from multiple_language import kevin_utils
from product_multiple_language import main_ui_2, find_translate_copy_rename
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QProgressDialog
import product_multiple_language.statistics_view
from multiple_language import multiple_language_utils
from product_multiple_language import statistics
import pyperclip


class MainWindow(QWidget, main_ui_2.Ui_Form):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.translate_statistics_list.keyPressEvent = self.__key_press_event

        self.input_string.insertFromMimeData = self.insertFromMimeData
        self.ignore_language_radio_button_list = [
            self.ignore_language_01,
            self.ignore_language_02,
            self.ignore_language_03,
            self.ignore_language_04,
            self.ignore_language_11,
            self.ignore_language_12,
            self.ignore_language_13,
            self.ignore_language_14
        ]

        _translate = QtCore.QCoreApplication.translate
        for i in range(len(multiple_language_utils.ignore_language_value_list)):
            kevin_utils.set_check_box_style(self.ignore_language_radio_button_list[i])
            language_text = multiple_language_utils.ignore_language_value_list[i]
            self.ignore_language_radio_button_list[i].setText(_translate("Form", language_text))
            self.ignore_language_radio_button_list[i].setChecked(True)
            if not self.ignore_language_text.toPlainText():
                self.ignore_language_text.setText(language_text)
            else:
                self.ignore_language_text.setText(self.ignore_language_text.toPlainText() + "/" + language_text)
            self.ignore_language_radio_button_list[i].toggled.connect(self.__add_ignore_language)
        # 隐藏多出来的按钮
        if len(self.ignore_language_radio_button_list) > len(multiple_language_utils.ignore_language_value_list):
            for i in range(len(self.ignore_language_radio_button_list)):
                if i >= len(multiple_language_utils.ignore_language_value_list):
                    self.ignore_language_radio_button_list[i].hide()
        self.ignore_language_select_all.clicked.connect(self.__select_all_ignore_language)

    def __add_ignore_language(self):
        self.ignore_language_text.setText("")
        for radio_button in self.ignore_language_radio_button_list:
            if radio_button.isChecked():
                if not self.ignore_language_text.toPlainText():
                    self.ignore_language_text.setText(radio_button.text())
                else:
                    self.ignore_language_text.setText(
                        self.ignore_language_text.toPlainText() + "/" + radio_button.text())

    def __select_all_ignore_language(self):
        self.ignore_language_text.setText("")
        select_all_enable = False
        for radio_button in self.ignore_language_radio_button_list:
            if not radio_button.isChecked():
                select_all_enable = True
        for radio_button in self.ignore_language_radio_button_list:
            radio_button.setChecked(select_all_enable)

    def insertFromMimeData(self, soc):
        if soc.hasText():
            # 去除粘贴格式
            self.input_string.textCursor().insertText(soc.text())

    def __key_press_event(self, event):
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_C:
            copy_string_list = ""
            for copy_string in self.translate_statistics_list.selectedItems():
                row = copy_string.row()
                copy_string_list += statistics.string_value_list[row] + "\n"
            pyperclip.copy(copy_string_list)
        else:
            super().keyPressEvent(event)


def find_translate(main_window: MainWindow):
    reply = QMessageBox.question(main_window, '查重拷贝字符', '确认查重拷贝吗', QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
    if reply == QMessageBox.Yes:
        translate_res_dir = main_window.input_translate_path.toPlainText().strip("\n")
        if translate_res_dir.startswith("file:///"):
            translate_res_dir = translate_res_dir[len("file:///"):]
        project_res_dir = main_window.input_project_path.toPlainText().strip("\n")
        if project_res_dir.startswith("file:///"):
            project_res_dir = project_res_dir[len("file:///"):]
        try:
            global progress_dialog
            progress_dialog = QProgressDialog(main_window)
            progress_dialog.setWindowTitle("查重拷贝字符")
            progress_dialog.setCancelButtonText("取消")
            progress_dialog.setMinimumDuration(5)
            progress_dialog.setWindowModality(Qt.WindowModal)
            progress_dialog.setRange(0, 100)
        except Exception as e:
            print(e)
        value = main_window.ignore_language_text.toPlainText()
        translate_string_list = find_translate_copy_rename.find_translate(
            translate_res_dir, project_res_dir, callback=progress_callback,
            ignore_language_list=value.split("/") if value else None)
        if translate_string_list:
            main_window.input_string.clear()
            main_window.input_string.append(translate_string_list)


def progress_callback(*args, **kwargs):
    if kwargs and "label" in kwargs:
        progress_dialog.setLabelText(kwargs["label"])
    if progress_dialog and isinstance(progress_dialog, QProgressDialog):
        progress_dialog.setValue(args[0] / args[1] * 100)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    desktop = app.desktop()
    width = desktop.width()
    height = desktop.height()

    window = MainWindow()
    x = int((width - window.frameGeometry().width()) / 2)
    y = int((height - window.frameGeometry().height()) / 2)
    window.move(x, y)
    window.show()
    window.setWindowTitle("产品多语言工具-为便捷而生")
    filename = kevin_utils.resource_path(os.path.join("ico", "logo.ico"))
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(filename))
    window.setWindowIcon(icon)

    multiple_language.main_window.init_view(window)
    product_multiple_language.statistics_view.init_view(window)
    window.check_copy_string.clicked.connect(lambda: find_translate(window))

    sys.exit(app.exec_())
