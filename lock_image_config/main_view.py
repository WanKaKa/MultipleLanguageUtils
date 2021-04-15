import os

from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5 import QtCore, QtGui

from lock_image_config import main_ui
from lock_image_config import utils
from lock_image_config import path
from lock_image_config import core
from lock_image_config import databases


class MainWindow(QWidget, main_ui.Ui_Form):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.select_service_url = None

        self.setWindowTitle("壁纸配置表自动修改-为便捷而生")
        filename = utils.resource_path(os.path.join("ico", "logo_image_config.ico"))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(filename))
        self.setWindowIcon(icon)

        self.init_view()

    def init_view(self):
        _translate = QtCore.QCoreApplication.translate
        self.service_url_1.setText(_translate("Form", "https://lockscreenres.oss-us-west-1.aliyuncs.com/"))
        self.service_url_2.setText(_translate("Form", "https://lockscreentabres.oss-us-west-1.aliyuncs.com/"))
        self.run_button.clicked.connect(self.run)
        self.log_button.clicked.connect(lambda: os.system(path.get_cache_path() + path.RUN_LOG_NAME))

        data = databases.get_normal_json_data()
        if data:
            if "service_dir_path" in data:
                self.service_image_path.setText(data["service_dir_path"])
            if "work_dir_path" in data:
                self.work_image_path.setText(data["work_dir_path"])

    def run(self):
        if not self.service_image_path.toPlainText():
            QMessageBox.information(self, '提示', '服务器壁纸路径为空!')
            return
        if not self.work_image_path.toPlainText():
            QMessageBox.information(self, '提示', '工作路径为空!')
            return
        if self.service_url_1.isChecked():
            self.select_service_url = self.service_url_1.text()
        elif self.service_url_2.isChecked():
            self.select_service_url = self.service_url_2.text()
        if not self.select_service_url:
            QMessageBox.information(self, '提示', '未选择服务器!')
            return
        reply = QMessageBox.question(
            self, '执行', '确认执行吗?', QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            service_image_path = self.service_image_path.toPlainText().strip("\n")
            if service_image_path.startswith("file:///"):
                service_image_path = service_image_path[len("file:///"):]
            work_image_path = self.work_image_path.toPlainText().strip("\n")
            if work_image_path.startswith("file:///"):
                work_image_path = work_image_path[len("file:///"):]
            databases.set_normal_json_data({"service_dir_path": service_image_path, "work_dir_path": work_image_path})
            log_file = open(path.get_cache_path() + path.RUN_LOG_NAME, mode='w', encoding='utf-8')
            core.run(service_image_path, work_image_path, self.select_service_url, log_file=log_file)
            log_file.close()
            QMessageBox.information(self, '提示', '壁纸配置修改成功!')
