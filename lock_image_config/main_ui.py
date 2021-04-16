# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(840, 440)
        self.formLayout = QtWidgets.QFormLayout(Form)
        self.formLayout.setObjectName("formLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setMinimumSize(QtCore.QSize(180, 80))
        self.label.setMaximumSize(QtCore.QSize(180, 16777215))
        self.label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 12pt \"微软雅黑\";")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.service_image_path = QtWidgets.QTextEdit(Form)
        self.service_image_path.setMinimumSize(QtCore.QSize(0, 80))
        self.service_image_path.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(85, 85, 255);\n"
"font: 12pt \"微软雅黑\";")
        self.service_image_path.setObjectName("service_image_path")
        self.horizontalLayout.addWidget(self.service_image_path)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setMinimumSize(QtCore.QSize(180, 80))
        self.label_2.setMaximumSize(QtCore.QSize(180, 16777215))
        self.label_2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 12pt \"微软雅黑\";")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_5.addWidget(self.label_2)
        self.work_image_path = QtWidgets.QTextEdit(Form)
        self.work_image_path.setMinimumSize(QtCore.QSize(0, 80))
        self.work_image_path.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(85, 85, 255);\n"
"font: 12pt \"微软雅黑\";")
        self.work_image_path.setObjectName("work_image_path")
        self.horizontalLayout_5.addWidget(self.work_image_path)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setMinimumSize(QtCore.QSize(180, 80))
        self.label_3.setMaximumSize(QtCore.QSize(180, 16777215))
        self.label_3.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 12pt \"微软雅黑\";")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.recommend_image_path = QtWidgets.QTextEdit(Form)
        self.recommend_image_path.setMinimumSize(QtCore.QSize(0, 80))
        self.recommend_image_path.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(85, 85, 255);\n"
"font: 12pt \"微软雅黑\";")
        self.recommend_image_path.setObjectName("recommend_image_path")
        self.horizontalLayout_3.addWidget(self.recommend_image_path)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setMinimumSize(QtCore.QSize(0, 80))
        self.frame.setMaximumSize(QtCore.QSize(16777215, 80))
        self.frame.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.service_url_1 = QtWidgets.QRadioButton(self.frame)
        self.service_url_1.setGeometry(QtCore.QRect(20, 0, 720, 40))
        self.service_url_1.setObjectName("service_url_1")
        self.service_url_2 = QtWidgets.QRadioButton(self.frame)
        self.service_url_2.setGeometry(QtCore.QRect(20, 40, 720, 40))
        self.service_url_2.setObjectName("service_url_2")
        self.horizontalLayout_2.addWidget(self.frame)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.frame_2 = QtWidgets.QFrame(Form)
        self.frame_2.setMinimumSize(QtCore.QSize(120, 50))
        self.frame_2.setMaximumSize(QtCore.QSize(120, 50))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.reset_button = QtWidgets.QPushButton(self.frame_2)
        self.reset_button.setGeometry(QtCore.QRect(0, 10, 120, 40))
        self.reset_button.setMinimumSize(QtCore.QSize(120, 40))
        self.reset_button.setMaximumSize(QtCore.QSize(120, 40))
        self.reset_button.setStyleSheet("background-color: rgb(255, 85, 127);\n"
"color: rgb(255, 255, 255);\n"
"font: 12pt \"微软雅黑\";")
        self.reset_button.setObjectName("reset_button")
        self.horizontalLayout_4.addWidget(self.frame_2)
        self.frame_3 = QtWidgets.QFrame(Form)
        self.frame_3.setMinimumSize(QtCore.QSize(0, 50))
        self.frame_3.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_4.addWidget(self.frame_3)
        self.frame_6 = QtWidgets.QFrame(Form)
        self.frame_6.setMinimumSize(QtCore.QSize(120, 50))
        self.frame_6.setMaximumSize(QtCore.QSize(120, 50))
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.run_button = QtWidgets.QPushButton(self.frame_6)
        self.run_button.setGeometry(QtCore.QRect(0, 10, 120, 40))
        self.run_button.setMinimumSize(QtCore.QSize(120, 40))
        self.run_button.setMaximumSize(QtCore.QSize(120, 40))
        self.run_button.setStyleSheet("background-color: rgb(85, 85, 255);\n"
"color: rgb(255, 255, 255);\n"
"font: 12pt \"微软雅黑\";")
        self.run_button.setObjectName("run_button")
        self.horizontalLayout_4.addWidget(self.frame_6)
        self.frame_5 = QtWidgets.QFrame(Form)
        self.frame_5.setMinimumSize(QtCore.QSize(0, 50))
        self.frame_5.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout_4.addWidget(self.frame_5)
        self.frame_8 = QtWidgets.QFrame(Form)
        self.frame_8.setMinimumSize(QtCore.QSize(120, 50))
        self.frame_8.setMaximumSize(QtCore.QSize(120, 50))
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")
        self.analysis_recommend_button = QtWidgets.QPushButton(self.frame_8)
        self.analysis_recommend_button.setGeometry(QtCore.QRect(0, 10, 120, 40))
        self.analysis_recommend_button.setMinimumSize(QtCore.QSize(120, 40))
        self.analysis_recommend_button.setMaximumSize(QtCore.QSize(120, 40))
        self.analysis_recommend_button.setStyleSheet("background-color: rgb(85, 85, 255);\n"
"color: rgb(255, 255, 255);\n"
"font: 12pt \"微软雅黑\";")
        self.analysis_recommend_button.setObjectName("analysis_recommend_button")
        self.horizontalLayout_4.addWidget(self.frame_8)
        self.frame_7 = QtWidgets.QFrame(Form)
        self.frame_7.setMinimumSize(QtCore.QSize(0, 50))
        self.frame_7.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.horizontalLayout_4.addWidget(self.frame_7)
        self.frame_4 = QtWidgets.QFrame(Form)
        self.frame_4.setMinimumSize(QtCore.QSize(120, 50))
        self.frame_4.setMaximumSize(QtCore.QSize(120, 50))
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.log_button = QtWidgets.QPushButton(self.frame_4)
        self.log_button.setGeometry(QtCore.QRect(0, 10, 120, 40))
        self.log_button.setMinimumSize(QtCore.QSize(120, 40))
        self.log_button.setMaximumSize(QtCore.QSize(120, 40))
        self.log_button.setStyleSheet("background-color: rgb(85, 85, 255);\n"
"color: rgb(255, 255, 255);\n"
"font: 12pt \"微软雅黑\";")
        self.log_button.setObjectName("log_button")
        self.horizontalLayout_4.addWidget(self.frame_4)
        self.frame_9 = QtWidgets.QFrame(Form)
        self.frame_9.setMinimumSize(QtCore.QSize(0, 50))
        self.frame_9.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_9.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_9.setObjectName("frame_9")
        self.horizontalLayout_4.addWidget(self.frame_9)
        self.frame_10 = QtWidgets.QFrame(Form)
        self.frame_10.setMinimumSize(QtCore.QSize(120, 50))
        self.frame_10.setMaximumSize(QtCore.QSize(120, 50))
        self.frame_10.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_10.setObjectName("frame_10")
        self.log_button_2 = QtWidgets.QPushButton(self.frame_10)
        self.log_button_2.setGeometry(QtCore.QRect(0, 10, 120, 40))
        self.log_button_2.setMinimumSize(QtCore.QSize(120, 40))
        self.log_button_2.setMaximumSize(QtCore.QSize(120, 40))
        self.log_button_2.setStyleSheet("background-color: rgb(85, 85, 255);\n"
"color: rgb(255, 255, 255);\n"
"font: 12pt \"微软雅黑\";")
        self.log_button_2.setObjectName("log_button_2")
        self.horizontalLayout_4.addWidget(self.frame_10)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.SpanningRole, self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "服务器壁纸路径"))
        self.label_2.setText(_translate("Form", "工作路径"))
        self.label_3.setText(_translate("Form", "推荐壁纸路径"))
        self.service_url_1.setText(_translate("Form", "RadioButton"))
        self.service_url_2.setText(_translate("Form", "RadioButton"))
        self.reset_button.setText(_translate("Form", "重置"))
        self.run_button.setText(_translate("Form", "处理壁纸"))
        self.analysis_recommend_button.setText(_translate("Form", "解析推荐壁纸"))
        self.log_button.setText(_translate("Form", "Log-处理壁纸"))
        self.log_button_2.setText(_translate("Form", "Log-推荐壁纸"))
