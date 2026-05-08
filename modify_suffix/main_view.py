import os
import shutil
import threading

import magic
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5 import QtGui
from filetype import filetype

from modify_suffix import main_ui, utils, path_ex, database

mime_map = {
    # ========== 文本类 ==========
    "text/plain": ".txt",
    "text/html": ".html",
    "text/css": ".css",
    "text/xml": ".xml",
    "text/csv": ".csv",
    "text/tab-separated-values": ".tsv",
    "text/javascript": ".js",
    "text/markdown": ".md",
    "text/rtf": ".rtf",

    # ========== 图片类 ==========
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/gif": ".gif",
    "image/bmp": ".bmp",
    "image/tiff": ".tiff",
    "image/webp": ".webp",
    "image/svg+xml": ".svg",
    "image/x-icon": ".ico",

    # ========== 音频类 ==========
    "audio/mpeg": ".mp3",
    "audio/wav": ".wav",
    "audio/flac": ".flac",
    "audio/ogg": ".ogg",
    "audio/aac": ".aac",
    "audio/x-ms-wma": ".wma",
    "audio/x-m4a": ".m4a",

    # ========== 视频类 ==========
    "video/mp4": ".mp4",
    "video/x-msvideo": ".avi",
    "video/x-ms-asf": ".asf",
    "video/x-ms-wmv": ".wmv",
    "video/3gpp": ".3gp",
    "video/quicktime": ".mov",
    "video/webm": ".webm",
    "video/mpeg": ".mpeg",

    # ========== Office 文档 ==========
    "application/msword": ".doc",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
    "application/vnd.ms-excel": ".xls",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
    "application/vnd.ms-powerpoint": ".ppt",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": ".pptx",
    "application/vnd.visio": ".vsd",
    "application/onenote": ".one",

    # ========== PDF / 电子书 ==========
    "application/pdf": ".pdf",
    "application/epub+zip": ".epub",
    "application/x-mobipocket-ebook": ".mobi",

    # ========== 压缩包 ==========
    "application/zip": ".zip",
    "application/x-rar-compressed": ".rar",
    "application/x-7z-compressed": ".7z",
    "application/x-gzip": ".gz",
    "application/x-tar": ".tar",
    "application/x-bzip2": ".bz2",

    # ========== 可执行 / 系统 ==========
    "application/x-msdownload": ".exe",
    "application/x-dosexec": ".exe",
    "application/x-ms-installer": ".msi",
    "application/x-shockwave-flash": ".swf",

    # ========== 字体 ==========
    "font/ttf": ".ttf",
    "font/otf": ".otf",
    "font/woff": ".woff",
    "font/woff2": ".woff2",

    # ========== 常见数据 / 配置 ==========
    "application/json": ".json",
    "application/zip-compressed": ".zip",
    "application/x-sqlite3": ".sqlite",
    "application/x-lua": ".lua",
    "application/x-python": ".py",
    "application/x-java": ".java",

    # ========== 你要的 trk（放在最后，避免覆盖） ==========
    "application/octet-stream": ".trk"
}


class MainWindow(QWidget, main_ui.Ui_Form):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.setWindowTitle("UI工具-为便捷而生")
        filename = utils.resource_path(os.path.join("image", "fast.ico"))
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

        log_file.write("\n\n")
        print("\n\n")

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
        if len(self.old_suffix) == 0 and len(self.new_suffix) == 0:
            QMessageBox.information(self, '提示', '"旧后缀""新后缀"不能同时都为空')
            return

        self.modify_suffix_task(self.work_path, self.old_suffix, self.new_suffix, log_file)
        log_file.close()
        QMessageBox.information(self, '提示', '成功')

    def bandizip_click(self):
        t = threading.Thread(target=self.bandizip_task)
        t.start()

    def bandizip_de_click(self):
        t = threading.Thread(target=self.bandizip_de_task)
        t.start()

    def delete_frame_click(self):
        log_file = open(path_ex.get_cache_path() + path_ex.LOG_DELETE_FRAME, mode='w', encoding='utf-8')
        self.get_input_value_list(log_file)
        if len(self.input_001_value) == 0:
            QMessageBox.information(self, '提示', '"旧文件名"不能为空')
            return
        self.delete_frame_task(self.work_path, self.input_001_value, log_file)
        log_file.close()
        QMessageBox.information(self, '提示', '成功')

    def modify_name_click(self):
        log_file = open(path_ex.get_cache_path() + path_ex.LOG_MODIFY_NAME, mode='w', encoding='utf-8')
        self.get_input_value_list(log_file)
        if len(self.input_001_value) == 0 or len(self.input_002_value) == 0:
            QMessageBox.information(self, '提示', '"旧文件名""新文件名"不能为空')
            return
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
                    if mime_type is None:
                        log_file.write("无法识别文件后缀：%s\n" % old_file)
                        print("无法识别文件后缀：%s\n" % old_file)
                        continue
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

    def delete_frame_task(self, dir_path, filter_value, log_file):
        file_list = os.listdir(dir_path)
        for file in file_list:
            old_file = os.path.join(dir_path, file)
            if os.path.isdir(old_file):
                self.delete_frame_task(old_file, filter_value, log_file)
            else:
                if filter_value in file:
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

    def bandizip_task(self):
        log_file = open(path_ex.get_cache_path() + path_ex.LOG_BANDIZIP, mode='w', encoding='utf-8')
        self.get_input_value_list(log_file)

        file_list = os.listdir(self.work_path)
        for file in file_list:
            old_file = os.path.join(self.work_path, file)
            if os.path.isdir(old_file):
                file_list_2 = os.listdir(old_file)
                # 判断是否有zip文件 无zip文件则返回
                has_zip = False
                for file_2 in file_list_2:
                    if ".zip" in file_2:
                        has_zip = True
                        break
                if has_zip:
                    value = "%s 有zip文件不压缩" % old_file
                    log_file.write("%s\n" % value)
                    print("%s\n" % value)
                    continue

                value = "bandizip.exe c " + old_file + "\\" + file + ".zip " + old_file
                log_file.write("%s\n" % value)
                print("%s\n" % value)
                os.system(value)

                for file_2 in file_list_2:
                    if os.path.isfile(old_file + "/" + file_2) and ".zip" not in file_2:
                        value = "del " + old_file + "\\" + file_2
                        log_file.write("删除文件 %s\n" % value)
                        print("删除文件 %s\n" % value)
                        os.system(value)
            log_file.write("\n\n")
            print("\n\n")
        log_file.close()
        # QMessageBox.information(self, '提示', '成功')

    def bandizip_de_task(self):
        log_file = open(path_ex.get_cache_path() + path_ex.LOG_BANDIZIP_DE, mode='w', encoding='utf-8')
        self.get_input_value_list(log_file)

        file_list = os.listdir(self.work_path)
        for file in file_list:
            old_file = os.path.join(self.work_path, file)
            if os.path.isdir(old_file):
                file_list_2 = os.listdir(old_file)
                # 判断是否有zip文件 无zip文件则返回
                has_zip = False
                for file_2 in file_list_2:
                    if ".zip" in file_2:
                        has_zip = True
                        break
                if not has_zip:
                    value = "%s 无zip文件不解压" % old_file
                    log_file.write("%s\n" % value)
                    print("%s\n" % value)
                    continue
                # 删除不是zip的文件
                for file_2 in file_list_2:
                    if os.path.isfile(old_file + "/" + file_2) and ".zip" not in file_2:
                        value = "del " + old_file + "\\" + file_2
                        log_file.write("删除文件 %s\n" % value)
                        print("删除文件 %s\n" % value)
                        os.system(value)
                value = "bandizip.exe x " + old_file + "\\" + file + ".zip " + old_file
                log_file.write("%s\n" % value)
                print("%s\n" % value)
                os.system(value)

                value = "del " + old_file + "\\" + file + ".zip"
                log_file.write("%s\n" % value)
                print("%s\n" % value)
                os.system(value)
            log_file.write("\n\n")
            print("\n\n")
        log_file.close()
        # QMessageBox.information(self, '提示', '成功')


def get_file_type(file_path):
    try:
        kind = filetype.guess(file_path)
        if kind:
            return kind.extension
        else:
            mime = magic.from_file(file_path, mime=True)
            if mime:
                return mime_map[mime]
    except Exception as e:
        print("错误:%s" % e)
    return None
