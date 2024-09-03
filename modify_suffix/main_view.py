import os
import shutil
import struct

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QMessageBox, QProgressDialog
from PyQt5 import QtCore, QtGui
from filetype import filetype

from modify_suffix import main_ui, utils, path_ex, database

MIME_TYPE_DICT = {
    '424D': 'bmp',
    'FFD8FF': 'jpg',
    '2E524D46': 'rm',
    '4D546864': 'mid',
    '89504E47': 'png',
    '47494638': 'gif',
    '49492A00': 'tif',
    '41433130': 'dwg',
    '38425053': 'psd',
    '2142444E': 'pst',
    'FF575043': 'wpd',
    'AC9EBD8F': 'qdf',
    'E3828596': 'pwl',
    '504B0304': 'zip',
    '52617221': 'rar',
    '57415645': 'wav',
    '41564920': 'avi',
    '2E7261FD': 'ram',
    '000001BA': 'mpg',
    '000001B3': 'mpg',
    '6D6F6F76': 'mov',
    '7B5C727466': 'rtf',
    '3C3F786D6C': 'xml',
    '68746D6C3E': 'html',
    'D0CF11E0': 'doc/xls',
    '255044462D312E': 'pdf',
    'CFAD12FEC5FD746F': 'dbx',
    '3026B2758E66CF11': 'asf',
    '5374616E64617264204A': 'mdb',
    '252150532D41646F6265': 'ps/eps',
    '44656C69766572792D646174653A': 'eml'
}


class MainWindow(QWidget, main_ui.Ui_Form):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.setWindowTitle("UI工具-为便捷而生")
        filename = utils.resource_path(os.path.join("ico", "fast.ico"))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(filename))
        self.setWindowIcon(icon)

        self.init_view()
        self.init_ui()

        self.input_001_value = None
        self.input_002_value = None
        self.input_003_value = None
        self.input_004_value = None
        self.input_005_value = None

        self.old_suffix = None
        self.new_suffix = None
        self.work_path = None

    def init_view(self):
        self.remove_suffix.clicked.connect(self.remove_suffix_click)
        self.add_suffix.clicked.connect(self.auto_add_suffix_click)
        self.modify_suffix.clicked.connect(self.modify_suffix_click)
        self.bandizip.clicked.connect(self.bandizip_click)
        self.bandizip_de.clicked.connect(self.bandizip_de_click)
        self.delete_frame.clicked.connect(self.delete_frame_click)
        self.modify_name.clicked.connect(self.modify_name_click)

        self.log_remove_suffix.clicked.connect(lambda: os.system(path_ex.get_cache_path() + path_ex.LOG_REMOVE_SUFFIX))
        self.log_add_suffix.clicked.connect(lambda: os.system(path_ex.get_cache_path() + path_ex.LOG_ADD_SUFFIX))
        self.log_modify_suffix.clicked.connect(lambda: os.system(path_ex.get_cache_path() + path_ex.LOG_MODIFY_SUFFIX))
        self.log_bandizip.clicked.connect(lambda: os.system(path_ex.get_cache_path() + path_ex.LOG_BANDIZIP))
        self.log_bandizip_de.clicked.connect(lambda: os.system(path_ex.get_cache_path() + path_ex.LOG_BANDIZIP_DE))
        self.log_delete_frame.clicked.connect(lambda: os.system(path_ex.get_cache_path() + path_ex.LOG_DELETE_FRAME))
        self.log_modify_name.clicked.connect(lambda: os.system(path_ex.get_cache_path() + path_ex.LOG_MODIFY_NAME))

    def init_ui(self):
        data = database.get_json_data()
        if data:
            if "input_001_value" in data:
                self.input_001.setText(data["input_001_value"].replace("\n", ""))
            if "input_002_value" in data:
                self.input_002.setText(data["input_002_value"].replace("\n", ""))
            if "input_003_value" in data:
                self.input_003.setText(data["input_003_value"].replace("\n", ""))
            if "input_004_value" in data:
                self.input_004.setText(data["input_004_value"].replace("\n", ""))
            if "input_005_value" in data:
                self.input_005.setText(data["input_005_value"].replace("\n", ""))

    def get_input_value_list(self, log_file):
        self.input_001_value = utils.analysis_input_path(self.input_001)
        self.input_002_value = utils.analysis_input_path(self.input_002)
        self.input_003_value = utils.analysis_input_path(self.input_003)
        self.input_004_value = utils.analysis_input_path(self.input_004)
        self.input_005_value = utils.analysis_input_path(self.input_005)

        data = {
            'input_001_value': self.input_001_value,
            'input_002_value': self.input_002_value,
            'input_003_value': self.input_003_value,
            'input_004_value': self.input_004_value,
            'input_005_value': self.input_005_value
        }
        database.set_json_data(data)

        self.old_suffix = self.input_003_value
        if self.old_suffix and "." not in self.old_suffix:
            self.old_suffix = "." + self.old_suffix
        log_file.write("旧后缀：%s\n" % self.old_suffix)
        print("旧后缀：%s\n" % self.old_suffix)

        self.new_suffix = self.input_004_value
        if self.new_suffix and "." not in self.new_suffix:
            self.new_suffix = "." + self.new_suffix
        log_file.write("新后缀：%s\n" % self.new_suffix)
        print("新后缀：%s\n" % self.new_suffix)

        self.work_path = self.input_005_value
        log_file.write("工作路径：%s\n" % self.work_path)
        print("工作路径：%s\n" % self.work_path)

    def remove_suffix_click(self):
        log_file = open(path_ex.get_cache_path() + path_ex.LOG_REMOVE_SUFFIX, mode='w', encoding='utf-8')
        self.get_input_value_list(log_file)
        self.modify_suffix_task(self.work_path, "", "", log_file)
        log_file.close()
        QMessageBox.information(self, '提示', '成功')

    def auto_add_suffix_click(self):
        log_file = open(path_ex.get_cache_path() + path_ex.LOG_ADD_SUFFIX, mode='w', encoding='utf-8')
        self.get_input_value_list(log_file)
        self.auto_add_suffix_task(self.work_path, log_file)
        log_file.close()
        QMessageBox.information(self, '提示', '成功')

    def modify_suffix_click(self):
        log_file = open(path_ex.get_cache_path() + path_ex.LOG_MODIFY_SUFFIX, mode='w', encoding='utf-8')
        self.get_input_value_list(log_file)
        self.modify_suffix_task(self.work_path, self.old_suffix, self.new_suffix, log_file)
        log_file.close()
        QMessageBox.information(self, '提示', '成功')

    def bandizip_click(self):
        log_file = open(path_ex.get_cache_path() + path_ex.LOG_BANDIZIP, mode='w', encoding='utf-8')
        self.get_input_value_list(log_file)
        bandizip_task(self.work_path, log_file)
        log_file.close()
        QMessageBox.information(self, '提示', '成功')

    def bandizip_de_click(self):
        log_file = open(path_ex.get_cache_path() + path_ex.LOG_BANDIZIP_DE, mode='w', encoding='utf-8')
        self.get_input_value_list(log_file)
        bandizip_de_task(self.work_path, log_file)
        log_file.close()
        QMessageBox.information(self, '提示', '成功')

    def delete_frame_click(self):
        log_file = open(path_ex.get_cache_path() + path_ex.LOG_DELETE_FRAME, mode='w', encoding='utf-8')
        self.get_input_value_list(log_file)
        self.delete_frame_task(self.work_path, log_file)
        log_file.close()
        QMessageBox.information(self, '提示', '成功')

    def modify_name_click(self):
        log_file = open(path_ex.get_cache_path() + path_ex.LOG_MODIFY_NAME, mode='w', encoding='utf-8')
        self.get_input_value_list(log_file)
        self.modify_name_task(self.work_path, self.input_001_value, self.input_002_value, log_file)
        log_file.close()
        QMessageBox.information(self, '提示', '成功')

    def modify_suffix_task(self, dir_path, old_suffix, new_suffix, log_file):
        file_list = os.listdir(dir_path)
        for file in file_list:
            old_file = os.path.join(dir_path, file)
            if os.path.isdir(old_file):
                self.modify_suffix_task(old_file, old_suffix, new_suffix, log_file)
            else:
                if old_suffix:
                    new_file = old_file.replace(old_suffix, new_suffix)
                else:
                    portion = os.path.splitext(old_file)
                    if not portion[1]:
                        # 文件没有扩展名
                        new_file = os.path.join(dir_path, file + new_suffix)
                    else:
                        new_file = old_file.replace(portion[1], new_suffix)

                log_file.write("原始文件：%s\n" % old_file)
                print("原始文件：%s\n" % old_file)

                log_file.write("修改文件：%s\n" % new_file)
                print("修改文件：%s\n" % new_file)

                shutil.move(old_file, new_file)

    def auto_add_suffix_task(self, dir_path, log_file):
        file_list = os.listdir(dir_path)
        for file in file_list:
            old_file = os.path.join(dir_path, file)
            if os.path.isdir(old_file):
                self.auto_add_suffix_task(old_file, log_file)
            else:
                portion = os.path.splitext(old_file)
                log_file.write("后缀名 = %s\n" % portion[1])
                print("后缀名 = %s\n" % portion[1])
                if not portion[1]:
                    log_file.write("后缀名空的文件 = %s\n" % old_file)
                    print("后缀名空的文件 = %s\n" % old_file)
                    mime_type = get_file_type(old_file)
                    if "." not in mime_type:
                        mime_type = "." + mime_type
                    log_file.write("文件类型 = %s\n" % mime_type)
                    print("文件类型 = %s\n" % mime_type)

                    new_file = os.path.join(dir_path, file + mime_type)

                    log_file.write("原始文件：%s\n" % old_file)
                    print("原始文件：%s\n" % old_file)

                    log_file.write("修改文件：%s\n" % new_file)
                    print("修改文件：%s\n" % new_file)

                    shutil.move(old_file, new_file)

    def delete_frame_task(self, dir_path, log_file):
        file_list = os.listdir(dir_path)
        for file in file_list:
            old_file = os.path.join(dir_path, file)
            if os.path.isdir(old_file):
                self.delete_frame_task(old_file, log_file)
            else:
                if "frame" in file:
                    log_file.write("%s\n" % old_file)
                    print("%s\n" % old_file)
                    os.remove(old_file)

    def modify_name_task(self, dir_path, old_name, new_name, log_file):
        if not old_name or not new_name:
            return
        file_list = os.listdir(dir_path)
        for file in file_list:
            old_file = os.path.join(dir_path, file)
            if os.path.isdir(old_file):
                self.modify_name_task(old_file, old_name, new_name, log_file)
            else:
                if old_name in file:
                    new_file = os.path.join(dir_path, new_name)
                    log_file.write("旧文件 = %s\n" % old_file)
                    print("旧文件 = %s\n" % old_file)
                    log_file.write("新文件 = %s\n" % new_file)
                    print("新文件 = %s\n" % new_file)
                    shutil.move(old_file, new_file)


def get_file_type(file_path):
    kind = filetype.guess(file_path)
    if kind:
        return kind.extension
    else:
        return 'unknown'


def bandizip_task(dir_path, log_file):
    file_list = os.listdir(dir_path)
    for file in file_list:
        old_file = os.path.join(dir_path, file)
        if os.path.isdir(old_file):
            value = "bandizip.exe c " + old_file + "/" + file + ".zip " + old_file
            log_file.write("%s\n" % value)
            print("%s\n" % value)
            os.system(value)


def bandizip_de_task(dir_path, log_file):
    file_list = os.listdir(dir_path)
    for file in file_list:
        old_file = os.path.join(dir_path, file)
        if os.path.isdir(old_file):
            # 删除不是zip的文件
            file_list_2 = os.listdir(old_file)
            for file_2 in file_list_2:
                print("%s\n" % file_2)
                if os.path.isfile(old_file + "/" + file_2) and ".zip" not in file_2:
                    value = "del " + old_file + "\\" + file_2
                    print("%s\n" % value)
                    os.system(value)
            value = "bandizip.exe x " + old_file + "\\" + file + ".zip " + old_file
            log_file.write("%s\n" % value)
            print("%s\n" % value)
            os.system(value)

            value = "del " + old_file + "\\" + file + ".zip"
            print("%s\n" % value)
            os.system(value)
