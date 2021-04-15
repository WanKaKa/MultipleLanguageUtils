import os
import sys

from PyQt5 import QtGui
from PyQt5.QtCore import Qt

import multiple_language.main_window
from multiple_language import kevin_utils
from product_multiple_language import main_ui_2, find_translate_copy_rename
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QProgressDialog
import product_multiple_language.statistics_view


class MainWindow(QWidget, main_ui_2.Ui_Form):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)


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
        translate_string_list = find_translate_copy_rename.find_translate(
            translate_res_dir, project_res_dir, callback=progress_callback)
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
