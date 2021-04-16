import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QMessageBox, QProgressDialog
from PyQt5 import QtCore, QtGui

from lock_image_config import main_ui
from lock_image_config import utils
from lock_image_config import path
from lock_image_config import core
from lock_image_config import databases
from lock_image_config import analysis_recommend


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

        self.progress_dialog = None
        self.init_view()

    def init_view(self):
        _translate = QtCore.QCoreApplication.translate
        self.service_url_1.setText(_translate("Form", "https://lockscreenres.oss-us-west-1.aliyuncs.com/"))
        self.service_url_2.setText(_translate("Form", "https://lockscreentabres.oss-us-west-1.aliyuncs.com/"))
        self.reset_button.clicked.connect(self.reset_work)
        self.run_button.clicked.connect(self.run)
        self.log_button.clicked.connect(lambda: os.system(path.get_cache_path() + path.RUN_LOG_NAME))
        self.log_button_2.clicked.connect(lambda: os.system(path.get_cache_path() + path.ANALYSIS_RECOMMEND_LOG_NAME))
        self.analysis_recommend_button.clicked.connect(self.analysis_recommend_image)

        data = databases.get_normal_json_data()
        if data:
            if "service_dir_path" in data:
                self.service_image_path.setText(data["service_dir_path"])
            if "work_dir_path" in data:
                self.work_image_path.setText(data["work_dir_path"])
            if "recommend_image_path" in data:
                self.recommend_image_path.setText(data["recommend_image_path"])

    def run(self):
        if self.tip_input():
            return
        reply = QMessageBox.question(
            self, '执行', '确认执行吗?', QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            service_image_path = utils.analysis_input_path(self.service_image_path)
            work_image_path = utils.analysis_input_path(self.work_image_path)
            # 保存数据
            databases.set_normal_json_data({"service_dir_path": service_image_path, "work_dir_path": work_image_path})
            log_file = open(path.get_cache_path() + path.RUN_LOG_NAME, mode='w', encoding='utf-8')
            self.init_progress_dialog()
            try:
                modify_success = True
                core.select_service_url = self.select_service_url
                core.run(service_image_path, work_image_path, log_file=log_file, callback=self.progress_callback)
            except Exception as e:
                modify_success = False
                utils.print_log(log_file, str(e))
                self.progress_callback(100, 100)
            log_file.close()
            QMessageBox.information(self, '提示', '壁纸配置修改成功!' if modify_success else "壁纸配置修改失败")

    def tip_input(self):
        if not self.service_image_path.toPlainText():
            QMessageBox.information(self, '提示', '服务器壁纸路径为空!')
            return True
        if not self.work_image_path.toPlainText():
            QMessageBox.information(self, '提示', '工作路径为空!')
            return True
        if self.service_url_1.isChecked():
            self.select_service_url = self.service_url_1.text()
        elif self.service_url_2.isChecked():
            self.select_service_url = self.service_url_2.text()
        if not self.select_service_url:
            QMessageBox.information(self, '提示', '未选择服务器!')
            return True
        return False

    def init_progress_dialog(self):
        self.progress_dialog = QProgressDialog(self)
        self.progress_dialog.setCancelButtonText("取消")
        self.progress_dialog.setMinimumDuration(5)
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.setRange(0, 100)

    def reset_work(self):
        reply = QMessageBox.question(
            self, '重置工作目录', '确定重置工作目录吗?', QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            work_image_path = utils.analysis_input_path(self.work_image_path)
            utils.delete_dir(work_image_path + "/xml/")
            QMessageBox.information(self, '提示', '工作目录已重置!')

    def analysis_recommend_image(self):
        if self.tip_input():
            return
        if not self.recommend_image_path.toPlainText():
            QMessageBox.information(self, '提示', '推荐壁纸路径为空!')
            return
        service_image_path = utils.analysis_input_path(self.service_image_path)
        work_image_path = utils.analysis_input_path(self.work_image_path)
        recommend_image_path = utils.analysis_input_path(self.recommend_image_path)
        databases.set_normal_json_data({"service_dir_path": service_image_path,
                                        "work_dir_path": work_image_path,
                                        "recommend_image_path": recommend_image_path})

        reply = QMessageBox.question(
            self, '推荐壁纸', '确认处理推荐壁纸吗?', QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            log_file = open(path.get_cache_path() + path.ANALYSIS_RECOMMEND_LOG_NAME, mode='w', encoding='utf-8')
            self.init_progress_dialog()
            core.select_service_url = self.select_service_url
            analysis_recommend.run(service_image_path, work_image_path,
                                   recommend_image_path, log_file=log_file, callback=self.progress_callback)
            log_file.close()
            QMessageBox.information(self, '提示', '推荐壁纸处理成功!')

    def progress_callback(self, *args, **kwargs):
        if self.progress_dialog and isinstance(self.progress_dialog, QProgressDialog):
            if kwargs and "label" in kwargs:
                self.progress_dialog.setLabelText(kwargs["label"])
            self.progress_dialog.setValue(min(100, args[0] / args[1] * 100))
