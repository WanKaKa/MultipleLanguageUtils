import json
import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QProgressDialog

from multiple_language import main_ui
from multiple_language import kevin_utils
from multiple_language import multiple_language_utils
from multiple_language import delete_res_string

progress_dialog = None


class MainWindow(QWidget, main_ui.Ui_Form):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)


def copy_multiple_language():
    reply = QMessageBox.question(
        main_window, '拷贝', '确定拷贝吗?', QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
    if reply == QMessageBox.Yes:
        input_strings = main_window.input_string.toPlainText().strip("\n")
        translate_dir = main_window.input_translate_path.toPlainText().strip("\n")
        if translate_dir.startswith("file:///"):
            translate_dir = translate_dir[len("file:///"):]
        project_dir = main_window.input_project_path.toPlainText().strip("\n")
        if project_dir.startswith("file:///"):
            project_dir = project_dir[len("file:///"):]
        try:
            global progress_dialog
            progress_dialog = QProgressDialog(main_window)
            progress_dialog.setWindowTitle("拷贝")
            progress_dialog.setLabelText("正在拷贝...")
            progress_dialog.setCancelButtonText("取消")
            progress_dialog.setMinimumDuration(5)
            progress_dialog.setWindowModality(Qt.WindowModal)
            progress_dialog.setRange(0, 100)
        except Exception as e:
            print(e)
        multiple_language_utils.copy_multiple_language(
            input_strings, translate_dir, project_dir, callback=progress_callback)


def delete_android_values_string():
    reply = QMessageBox.question(
        main_window, '删除', '确定删除吗?', QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
    if reply == QMessageBox.Yes:
        input_strings = main_window.input_string.toPlainText().strip("\n")
        project_dir = main_window.input_project_path.toPlainText().strip("\n")
        if project_dir.startswith("file:///"):
            project_dir = project_dir[len("file:///"):]
        try:
            global progress_dialog
            progress_dialog = QProgressDialog(main_window)
            progress_dialog.setWindowTitle("删除")
            progress_dialog.setLabelText("正在删除...")
            progress_dialog.setCancelButtonText("取消")
            progress_dialog.setMinimumDuration(5)
            progress_dialog.setWindowModality(Qt.WindowModal)
            progress_dialog.setRange(0, 100)
        except Exception as e:
            print(e)
        delete_res_string.delete_android_values_string(project_dir, input_strings, callback=progress_callback)


def progress_callback(total, progress):
    if progress_dialog and isinstance(progress_dialog, QProgressDialog):
        progress_dialog.setValue(progress / total * 100)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    desktop = app.desktop()
    width = desktop.width()
    height = desktop.height()

    main_window = MainWindow()
    main_window.show()
    main_window.move(int((width - 1080) / 2), int((height - 720) / 2))
    main_window.setWindowTitle("翻译拷贝程序-为便捷而生")
    filename = kevin_utils.resource_path(os.path.join("ico", "logo_multiple_language.ico"))
    icon = QIcon()
    icon.addPixmap(QPixmap(filename))
    main_window.setWindowIcon(icon)

    main_window.copy_translate_path.clicked.connect(
        lambda: main_window.input_translate_path.setText(main_window.old_translate_path.text()))
    main_window.copy_project_path.clicked.connect(
        lambda: main_window.input_project_path.setText(main_window.old_project_path.text()))

    main_window.copy_string.clicked.connect(copy_multiple_language)
    main_window.delete_string.clicked.connect(delete_android_values_string)
    main_window.open_copy_logo.clicked.connect(lambda: kevin_utils.open_file(
        kevin_utils.get_log_path() + multiple_language_utils.language_log_name))
    main_window.open_delete_log.clicked.connect(lambda: kevin_utils.open_file(
        kevin_utils.get_log_path() + delete_res_string.log_delete_res_string))

    if os.path.exists(kevin_utils.get_log_path() + multiple_language_utils.database_name):
        read_data = open(kevin_utils.get_log_path() + multiple_language_utils.database_name, mode='r', encoding='utf-8')
        try:
            data = json.loads(read_data.read())
            main_window.input_string.setText(data["translate_string"])
            main_window.old_translate_path.setText(data["translate_res_dir"].replace("\n", ""))
            if not main_window.old_translate_path.text():
                main_window.copy_translate_path.hide()
            main_window.old_project_path.setText(data["project_res_dir"].replace("\n", ""))
            if not main_window.old_project_path.text():
                main_window.copy_project_path.hide()
        finally:
            pass
        read_data.close()
    sys.exit(app.exec_())
