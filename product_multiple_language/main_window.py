import os
import sys

from PyQt5 import QtGui
from PyQt5.QtCore import Qt

from multiple_language import kevin_utils
from multiple_language.main_window import MainWindowFactory
from product_multiple_language import main_ui_2, find_translate_copy_rename
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
import product_multiple_language.statistics_view
from product_multiple_language import statistics
import pyperclip


class MainWindow(QWidget, main_ui_2.Ui_Form):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.translate_statistics_list.keyPressEvent = self.__key_press_event

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
            main_window_factory.progress_dialog.setWindowTitle("查重拷贝字符")
            main_window_factory.progress_dialog.setCancelButtonText("取消")
        except Exception as e:
            print(e)
        value = main_window.ignore_language_text.toPlainText()
        translate_string_list = find_translate_copy_rename.find_translate(
            translate_res_dir, project_res_dir, callback=main_window_factory.progress_callback,
            ignore_language_list=value.split("/") if value else None)
        if translate_string_list:
            main_window.input_string.clear()
            main_window.input_string.append(translate_string_list)


if __name__ == "__main__":
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
    window.setWindowTitle("产品多语言工具-为便捷而生")

    icon_name = kevin_utils.resource_path(os.path.join("ico", "logo.ico"))
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(icon_name))
    window.setWindowIcon(icon)

    main_window_factory = MainWindowFactory(window)
    product_multiple_language.statistics_view.init_view(window)
    window.check_copy_string.clicked.connect(lambda: find_translate(window))

    sys.exit(app.exec_())
