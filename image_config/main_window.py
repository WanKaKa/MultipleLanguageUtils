import os
import sys
import xml.dom.minidom

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QDialog
from PyQt5 import QtCore
from natsort import ns, natsorted

from image_config import select_dialog_ui
from image_config import main_ui

server_name_list = [
    "https://lockscreenres.oss-us-west-1.aliyuncs.com/",
    "https://lockscreentabres.oss-us-west-1.aliyuncs.com/"
]
server_radio_button_list = []
skin_dir_list = []
skin_config_list = []


class MainWindow(QMainWindow, main_ui.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)


class ServerWindow(QDialog, select_dialog_ui.Ui_Form):
    def __init__(self, parent=None):
        super(ServerWindow, self).__init__(parent)
        self.setupUi(self)


class SkinItem:
    def __init__(self, download_url="", from_type="", skin_id="", thumb="", url=""):
        self.download_url = download_url
        self.from_type = from_type
        self.skin_id = skin_id
        self.thumb = thumb
        self.url = url


# 选取文件夹
def set_root_dir():
    if os.path.exists(main_window.label_2.text()):
        dir_path = QFileDialog.getExistingDirectory(main_window, "选取文件夹", main_window.label_2.text())
    else:
        dir_path = QFileDialog.getExistingDirectory(main_window, "选取文件夹", os.getcwd())
    if dir_path:
        main_window.label_2.setText(dir_path)
        print_log(dir_path)
        print_log("\n" * 3)
        analysis_skin_config()


def set_server():
    server_window = ServerWindow(main_window)
    server_window.show()
    server_window.move(int((width - 300) / 2), int((height - 640) / 2))
    server_window.setWindowTitle("选择服务器-为便捷而生")
    server_window.setWindowIcon(QIcon('favicon.ico'))

    global server_radio_button_list
    server_radio_button_list = [
        server_window.radioButton,
        server_window.radioButton_2,
        server_window.radioButton_3,
        server_window.radioButton_4,
        server_window.radioButton_5,
        server_window.radioButton_6,
        server_window.radioButton_7,
        server_window.radioButton_8,
        server_window.radioButton_9,
        server_window.radioButton_10,
        server_window.radioButton_11,
        server_window.radioButton_12,
        server_window.radioButton_13,
        server_window.radioButton_14,
        server_window.radioButton_15,
        server_window.radioButton_16
    ]
    # 设置按钮状态和点击事件
    _translate = QtCore.QCoreApplication.translate
    for i in range(len(server_name_list)):
        server_radio_button_list[i].setText(_translate("Form", server_name_list[i]))
        server_radio_button_list[i].toggled.connect(lambda: get_server(server_window))
        server_radio_button_list[i].setChecked(main_window.label_4.text() == server_name_list[i])
    # 隐藏多出来的按钮
    if len(server_radio_button_list) > len(server_name_list):
        for i in range(len(server_radio_button_list)):
            if i >= len(server_name_list):
                server_radio_button_list[i].hide()
    server_window.exec()


def get_server(server_window):
    for radio_button in server_radio_button_list:
        if radio_button.isChecked():
            main_window.label_4.setText(radio_button.text())
            server_window.close()


def analysis_skin_config():
    for root, dirs, files in os.walk(main_window.label_2.text() + "\\" + "xml"):
        global skin_config_list
        if files:
            skin_config_list = files
            skin_config_list = natsorted(skin_config_list, alg=ns.PATH)
    print_log(skin_config_list)
    print_log("\n" * 3)
    skin_dir_list.clear()
    for file in natsorted(os.listdir(main_window.label_2.text()), alg=ns.PATH):
        if file and file not in ["xml", "skin_thumb", "version.xml"]:
            skin_dir_list.append(file)
    print_log(skin_dir_list)
    print_log("\n" * 3)


def start_modify_config():
    if not main_window.label_2.text() or not main_window.label_4.text():
        return

    main_window.pushButton_3.setText("处理中...")
    for skin_name in skin_dir_list:
        print_log("处理壁纸类型: %s" % skin_name)
        path = main_window.label_2.text() + "/xml/skin_" + skin_name + ".xml"
        dom = xml.dom.minidom.parse(path)
        root = dom.documentElement
        skin_list = root.getElementsByTagName('item')

        last_index = 0
        for item in skin_list:
            str_index = str(item.getAttribute("download_url").split("_")[1])
            if "." in str_index:
                tempIndex = int(str_index.split(".")[0])
            else:
                tempIndex = int(str_index)
            if tempIndex >= last_index:
                last_index = tempIndex

        new_skin_count = len(os.listdir(main_window.label_2.text() + "/" + skin_name))
        print_log("新壁纸数量 = %d；配置文件壁纸最大的index = %d" % (new_skin_count, last_index))
        print_log("\n")
        modify_item_xml(skin_name, last_index, new_skin_count)
        modify_skin_name(skin_name, last_index, new_skin_count)
        modify_thumb_name(skin_name, last_index, new_skin_count)
        print_log("\n" * 3)
    main_window.pushButton_3.setText("开始")


# 修改壁纸配置表
def modify_item_xml(skin_name, last_index, new_skin_count):
    print_log("配置文件--开始")
    old_path = main_window.label_2.text() + "/xml/skin_" + skin_name + ".xml"
    old_file = open(old_path, mode='r', encoding='utf-8')
    new_path = main_window.label_2.text() + "/xml/skin_" + skin_name + ".xml.ijs"
    new_file = open(new_path, mode='w', encoding='utf-8')
    line = old_file.readline()
    while line:
        new_file.write(line)
        if line.replace("\n", "") == "<skin>":
            for i in range(new_skin_count):
                new_file.write(create_xml_item(skin_name, last_index + 1 + i))
        line = old_file.readline()
    old_file.close()
    new_file.close()
    os.remove(old_path)
    os.rename(new_path, old_path)
    print_log("配置文件--结束")
    print_log("\n")


# 修改壁纸名称
def modify_skin_name(skin_name, last_index, new_skin_count):
    print_log("壁纸处理--开始")
    image_path = main_window.label_2.text() + "/" + skin_name + "/"
    image_files = natsorted(os.listdir(image_path), alg=ns.PATH)
    index = new_skin_count - 1
    while index >= 0:
        new_index = last_index + 1 + index
        if "." in image_files:
            new_name = image_path + skin_name + "_" + int2str(new_index) + "." + image_files[index].split(".")[1]
        else:
            new_name = image_path + skin_name + "_" + int2str(new_index)
        if os.path.exists(new_name):
            break
        os.rename(image_path + image_files[index], new_name)
        print_log("旧: %s" % image_path + image_files[index])
        print_log("新: %s" % new_name)
        print_log("-" * 50)
        index -= 1
    print_log("壁纸处理--结束")
    print_log("\n")


# 修改壁纸名称
def modify_thumb_name(skin_name, last_index, new_skin_count):
    print_log("缩略图--开始")
    thumb_path = main_window.label_2.text() + "/skin_thumb/" + skin_name + "/"
    thumb_files = natsorted(os.listdir(thumb_path), alg=ns.PATH)
    index = new_skin_count - 1
    while index >= 0:
        new_index = last_index + 1 + index
        if "." in thumb_files:
            new_name = thumb_path + skin_name + "_" + int2str(new_index) + "." + thumb_files[index].split(".")[1]
        else:
            new_name = thumb_path + skin_name + "_" + int2str(new_index)
        if os.path.exists(new_name):
            break
        os.rename(thumb_path + thumb_files[index], new_name)
        print_log("旧: %s" % thumb_path + thumb_files[index])
        print_log("新: %s" % new_name)
        print_log("-" * 50)
        index -= 1
    print_log("缩略图--结束")
    print_log("\n")


def create_xml_item(skin_name, index):
    server = main_window.label_4.text()
    download_url = server + skin_name + "/" + skin_name + "_" + int2str(index)
    thumb = server + "skin_thumb/" + skin_name + "/" + skin_name + "_" + int2str(index)
    url = "skin_img/" + skin_name + "/" + skin_name + "_" + int2str(index) + ".ijs"
    item_str = "    <item" + "\n"
    item_str += "        download_url=" + "\"" + download_url + "\"\n"
    item_str += "        from=" + "\"" + "net" + "\"\n"
    item_str += "        id=" + "\"" + str((index - 1)) + "\"\n"
    item_str += "        thumb=" + "\"" + thumb + "\"\n"
    item_str += "        url=" + "\"" + url + "\" />\n"
    return item_str


def print_log(log):
    print(log)
    main_window.textBrowser.append(str(log))


def int2str(index):
    if index < 10:
        return "0" + str(index)
    return str(index)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    desktop = app.desktop()
    width = desktop.width()
    height = desktop.height()

    main_window = MainWindow()
    main_window.show()
    main_window.move(int((width - 800) / 2), int((height - 800) / 2))
    main_window.setFixedSize(main_window.width(), main_window.height())
    main_window.setWindowTitle("壁纸配置表自动修改-为便捷而生")
    main_window.setWindowIcon(QIcon('favicon.ico'))

    main_window.pushButton.clicked.connect(set_root_dir)
    main_window.pushButton_2.clicked.connect(set_server)
    main_window.pushButton_3.clicked.connect(start_modify_config)

    sys.exit(app.exec_())
