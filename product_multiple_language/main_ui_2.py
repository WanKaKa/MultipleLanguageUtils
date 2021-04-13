# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_ui_2.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1800, 900)
        Form.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.formLayout = QtWidgets.QFormLayout(Form)
        self.formLayout.setObjectName("formLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setMinimumSize(QtCore.QSize(0, 40))
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 40))
        self.label_3.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(85, 85, 255);\n"
"font: 16pt \"微软雅黑\";")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setMinimumSize(QtCore.QSize(50, 40))
        self.label_8.setMaximumSize(QtCore.QSize(50, 40))
        self.label_8.setStyleSheet("font: 12pt \"微软雅黑\";\n"
"background-color: rgb(255, 255, 255);")
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_2.addWidget(self.label_8)
        self.compete_string_dir = QtWidgets.QLabel(Form)
        self.compete_string_dir.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 12pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.compete_string_dir.setText("")
        self.compete_string_dir.setAlignment(QtCore.Qt.AlignCenter)
        self.compete_string_dir.setObjectName("compete_string_dir")
        self.horizontalLayout_2.addWidget(self.compete_string_dir)
        self.compete_string_click_select_dir = QtWidgets.QPushButton(Form)
        self.compete_string_click_select_dir.setMinimumSize(QtCore.QSize(80, 40))
        self.compete_string_click_select_dir.setMaximumSize(QtCore.QSize(80, 40))
        self.compete_string_click_select_dir.setStyleSheet("background-color: rgb(85, 85, 255);\n"
"color: rgb(255, 255, 255);\n"
"font: 12pt \"微软雅黑\";")
        self.compete_string_click_select_dir.setObjectName("compete_string_click_select_dir")
        self.horizontalLayout_2.addWidget(self.compete_string_click_select_dir)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.compete_string_find_string = QtWidgets.QLineEdit(Form)
        self.compete_string_find_string.setMinimumSize(QtCore.QSize(0, 40))
        self.compete_string_find_string.setMaximumSize(QtCore.QSize(16777215, 40))
        self.compete_string_find_string.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 12pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.compete_string_find_string.setObjectName("compete_string_find_string")
        self.horizontalLayout_7.addWidget(self.compete_string_find_string)
        self.compete_string_click_find = QtWidgets.QPushButton(Form)
        self.compete_string_click_find.setMinimumSize(QtCore.QSize(80, 40))
        self.compete_string_click_find.setMaximumSize(QtCore.QSize(80, 40))
        self.compete_string_click_find.setStyleSheet("background-color: rgb(85, 85, 255);\n"
"color: rgb(255, 255, 255);\n"
"font: 12pt \"微软雅黑\";")
        self.compete_string_click_find.setObjectName("compete_string_click_find")
        self.horizontalLayout_7.addWidget(self.compete_string_click_find)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.compete_string_list = QtWidgets.QTableWidget(Form)
        self.compete_string_list.setObjectName("compete_string_list")
        self.compete_string_list.setColumnCount(0)
        self.compete_string_list.setRowCount(0)
        self.verticalLayout.addWidget(self.compete_string_list)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_9 = QtWidgets.QLabel(Form)
        self.label_9.setMinimumSize(QtCore.QSize(120, 40))
        self.label_9.setMaximumSize(QtCore.QSize(120, 40))
        self.label_9.setStyleSheet("font: 12pt \"微软雅黑\";\n"
"background-color: rgb(255, 255, 255);")
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_3.addWidget(self.label_9)
        self.compete_string_need_rename = QtWidgets.QLineEdit(Form)
        self.compete_string_need_rename.setMinimumSize(QtCore.QSize(0, 40))
        self.compete_string_need_rename.setMaximumSize(QtCore.QSize(16777215, 40))
        self.compete_string_need_rename.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 12pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.compete_string_need_rename.setObjectName("compete_string_need_rename")
        self.horizontalLayout_3.addWidget(self.compete_string_need_rename)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_11 = QtWidgets.QLabel(Form)
        self.label_11.setMinimumSize(QtCore.QSize(120, 40))
        self.label_11.setMaximumSize(QtCore.QSize(120, 40))
        self.label_11.setStyleSheet("font: 12pt \"微软雅黑\";\n"
"background-color: rgb(255, 255, 255);")
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_5.addWidget(self.label_11)
        self.project_string_name = QtWidgets.QLineEdit(Form)
        self.project_string_name.setMinimumSize(QtCore.QSize(0, 40))
        self.project_string_name.setMaximumSize(QtCore.QSize(16777215, 40))
        self.project_string_name.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 12pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.project_string_name.setObjectName("project_string_name")
        self.horizontalLayout_5.addWidget(self.project_string_name)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setMinimumSize(QtCore.QSize(0, 50))
        self.frame.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_6.addWidget(self.frame)
        self.frame_6 = QtWidgets.QFrame(Form)
        self.frame_6.setMinimumSize(QtCore.QSize(240, 50))
        self.frame_6.setMaximumSize(QtCore.QSize(240, 50))
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.compete_string_click_rename = QtWidgets.QPushButton(self.frame_6)
        self.compete_string_click_rename.setGeometry(QtCore.QRect(0, 10, 100, 40))
        self.compete_string_click_rename.setStyleSheet("background-color: rgb(85, 85, 255);\n"
"font: 12pt \"微软雅黑\";\n"
"color: rgb(255, 255, 255);")
        self.compete_string_click_rename.setObjectName("compete_string_click_rename")
        self.compete_string_click_refresh = QtWidgets.QPushButton(self.frame_6)
        self.compete_string_click_refresh.setGeometry(QtCore.QRect(140, 10, 100, 40))
        self.compete_string_click_refresh.setStyleSheet("background-color: rgb(85, 85, 255);\n"
"font: 12pt \"微软雅黑\";\n"
"color: rgb(255, 255, 255);")
        self.compete_string_click_refresh.setObjectName("compete_string_click_refresh")
        self.horizontalLayout_6.addWidget(self.frame_6)
        self.frame_7 = QtWidgets.QFrame(Form)
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.horizontalLayout_6.addWidget(self.frame_7)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(Form)
        self.label.setMinimumSize(QtCore.QSize(600, 40))
        self.label.setMaximumSize(QtCore.QSize(600, 40))
        self.label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(85, 85, 255);\n"
"font: 16pt \"微软雅黑\";")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setMinimumSize(QtCore.QSize(600, 40))
        self.label_2.setMaximumSize(QtCore.QSize(600, 40))
        self.label_2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 10pt \"微软雅黑\";")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.input_string = QtWidgets.QTextEdit(Form)
        self.input_string.setMinimumSize(QtCore.QSize(600, 0))
        self.input_string.setMaximumSize(QtCore.QSize(600, 16777215))
        self.input_string.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 10pt \"微软雅黑\";")
        self.input_string.setObjectName("input_string")
        self.verticalLayout_2.addWidget(self.input_string)
        self.frame_3 = QtWidgets.QFrame(Form)
        self.frame_3.setMinimumSize(QtCore.QSize(0, 40))
        self.frame_3.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frame_3.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.label_7 = QtWidgets.QLabel(self.frame_3)
        self.label_7.setGeometry(QtCore.QRect(0, 0, 80, 40))
        self.label_7.setMinimumSize(QtCore.QSize(80, 40))
        self.label_7.setMaximumSize(QtCore.QSize(80, 40))
        self.label_7.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 10pt \"微软雅黑\";")
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.copy_translate_path = QtWidgets.QPushButton(self.frame_3)
        self.copy_translate_path.setGeometry(QtCore.QRect(520, 5, 75, 30))
        self.copy_translate_path.setStyleSheet("background-color: rgb(85, 85, 255);\n"
"font: 12pt \"微软雅黑\";\n"
"color: rgb(255, 255, 255);")
        self.copy_translate_path.setObjectName("copy_translate_path")
        self.old_translate_path = QtWidgets.QLabel(self.frame_3)
        self.old_translate_path.setGeometry(QtCore.QRect(80, 0, 440, 40))
        self.old_translate_path.setMinimumSize(QtCore.QSize(440, 40))
        self.old_translate_path.setMaximumSize(QtCore.QSize(440, 40))
        self.old_translate_path.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 8pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.old_translate_path.setText("")
        self.old_translate_path.setAlignment(QtCore.Qt.AlignCenter)
        self.old_translate_path.setObjectName("old_translate_path")
        self.verticalLayout_2.addWidget(self.frame_3)
        self.input_translate_path = QtWidgets.QTextEdit(Form)
        self.input_translate_path.setMinimumSize(QtCore.QSize(0, 60))
        self.input_translate_path.setMaximumSize(QtCore.QSize(600, 60))
        self.input_translate_path.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(85, 85, 255);\n"
"font: 12pt \"微软雅黑\";")
        self.input_translate_path.setObjectName("input_translate_path")
        self.verticalLayout_2.addWidget(self.input_translate_path)
        self.frame_4 = QtWidgets.QFrame(Form)
        self.frame_4.setMinimumSize(QtCore.QSize(0, 40))
        self.frame_4.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frame_4.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.label_6 = QtWidgets.QLabel(self.frame_4)
        self.label_6.setGeometry(QtCore.QRect(0, 0, 80, 40))
        self.label_6.setMinimumSize(QtCore.QSize(80, 40))
        self.label_6.setMaximumSize(QtCore.QSize(80, 40))
        self.label_6.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 10pt \"微软雅黑\";")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.copy_project_path = QtWidgets.QPushButton(self.frame_4)
        self.copy_project_path.setGeometry(QtCore.QRect(520, 5, 75, 30))
        self.copy_project_path.setStyleSheet("background-color: rgb(85, 85, 255);\n"
"font: 12pt \"微软雅黑\";\n"
"color: rgb(255, 255, 255);")
        self.copy_project_path.setObjectName("copy_project_path")
        self.old_project_path = QtWidgets.QLabel(self.frame_4)
        self.old_project_path.setGeometry(QtCore.QRect(80, 0, 440, 40))
        self.old_project_path.setMinimumSize(QtCore.QSize(440, 40))
        self.old_project_path.setMaximumSize(QtCore.QSize(440, 40))
        self.old_project_path.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 8pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.old_project_path.setText("")
        self.old_project_path.setAlignment(QtCore.Qt.AlignCenter)
        self.old_project_path.setObjectName("old_project_path")
        self.verticalLayout_2.addWidget(self.frame_4)
        self.input_project_path = QtWidgets.QTextEdit(Form)
        self.input_project_path.setMinimumSize(QtCore.QSize(0, 60))
        self.input_project_path.setMaximumSize(QtCore.QSize(600, 60))
        self.input_project_path.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 12pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.input_project_path.setObjectName("input_project_path")
        self.verticalLayout_2.addWidget(self.input_project_path)
        self.frame_2 = QtWidgets.QFrame(Form)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 50))
        self.frame_2.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.delete_string = QtWidgets.QPushButton(self.frame_2)
        self.delete_string.setGeometry(QtCore.QRect(250, 10, 100, 40))
        self.delete_string.setStyleSheet("background-color: rgb(255, 85, 127);\n"
"font: 12pt \"微软雅黑\";\n"
"color: rgb(255, 255, 255);")
        self.delete_string.setObjectName("delete_string")
        self.copy_string = QtWidgets.QPushButton(self.frame_2)
        self.copy_string.setGeometry(QtCore.QRect(125, 10, 100, 40))
        self.copy_string.setStyleSheet("background-color: rgb(85, 85, 255);\n"
"font: 12pt \"微软雅黑\";\n"
"color: rgb(255, 255, 255);")
        self.copy_string.setObjectName("copy_string")
        self.open_copy_logo = QtWidgets.QPushButton(self.frame_2)
        self.open_copy_logo.setGeometry(QtCore.QRect(375, 10, 100, 40))
        self.open_copy_logo.setStyleSheet("background-color: rgb(85, 85, 255);\n"
"font: 12pt \"微软雅黑\";\n"
"color: rgb(255, 255, 255);")
        self.open_copy_logo.setObjectName("open_copy_logo")
        self.open_delete_log = QtWidgets.QPushButton(self.frame_2)
        self.open_delete_log.setGeometry(QtCore.QRect(500, 10, 100, 40))
        self.open_delete_log.setStyleSheet("background-color: rgb(85, 85, 255);\n"
"font: 12pt \"微软雅黑\";\n"
"color: rgb(255, 255, 255);")
        self.open_delete_log.setObjectName("open_delete_log")
        self.check_copy_string = QtWidgets.QPushButton(self.frame_2)
        self.check_copy_string.setGeometry(QtCore.QRect(0, 10, 100, 40))
        self.check_copy_string.setStyleSheet("background-color: rgb(85, 85, 255);\n"
"font: 12pt \"微软雅黑\";\n"
"color: rgb(255, 255, 255);")
        self.check_copy_string.setObjectName("check_copy_string")
        self.verticalLayout_2.addWidget(self.frame_2)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setMinimumSize(QtCore.QSize(600, 40))
        self.label_4.setMaximumSize(QtCore.QSize(600, 40))
        self.label_4.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(85, 85, 255);\n"
"font: 16pt \"微软雅黑\";")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
        self.translate_statistics = QtWidgets.QTextBrowser(Form)
        self.translate_statistics.setMinimumSize(QtCore.QSize(600, 0))
        self.translate_statistics.setMaximumSize(QtCore.QSize(600, 16777215))
        self.translate_statistics.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.translate_statistics.setObjectName("translate_statistics")
        self.verticalLayout_3.addWidget(self.translate_statistics)
        self.frame_5 = QtWidgets.QFrame(Form)
        self.frame_5.setMinimumSize(QtCore.QSize(0, 50))
        self.frame_5.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.refersh_translate_statistics = QtWidgets.QPushButton(self.frame_5)
        self.refersh_translate_statistics.setGeometry(QtCore.QRect(250, 10, 100, 40))
        self.refersh_translate_statistics.setStyleSheet("background-color: rgb(85, 85, 255);\n"
"font: 12pt \"微软雅黑\";\n"
"color: rgb(255, 255, 255);")
        self.refersh_translate_statistics.setObjectName("refersh_translate_statistics")
        self.verticalLayout_3.addWidget(self.frame_5)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.SpanningRole, self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_3.setText(_translate("Form", "手动查找"))
        self.label_8.setText(_translate("Form", "路径"))
        self.compete_string_click_select_dir.setText(_translate("Form", "选择"))
        self.compete_string_click_find.setText(_translate("Form", "查找"))
        self.label_9.setText(_translate("Form", "竞争产品字符"))
        self.label_11.setText(_translate("Form", "项目字符"))
        self.compete_string_click_rename.setText(_translate("Form", "重命名字符"))
        self.compete_string_click_refresh.setText(_translate("Form", "刷新"))
        self.label.setText(_translate("Form", "拷贝区域"))
        self.label_2.setText(_translate("Form", "需要拷贝的字符，格式如下：<string name=\"i_joy_soft\">IJoySoft</string>"))
        self.label_7.setText(_translate("Form", "翻译路径:"))
        self.copy_translate_path.setText(_translate("Form", "使用"))
        self.label_6.setText(_translate("Form", "项目路径:"))
        self.copy_project_path.setText(_translate("Form", "使用"))
        self.delete_string.setText(_translate("Form", "删除"))
        self.copy_string.setText(_translate("Form", "拷贝"))
        self.open_copy_logo.setText(_translate("Form", "Log-拷贝"))
        self.open_delete_log.setText(_translate("Form", "Log-删除"))
        self.check_copy_string.setText(_translate("Form", "查重拷贝"))
        self.label_4.setText(_translate("Form", "翻译统计区域"))
        self.refersh_translate_statistics.setText(_translate("Form", "刷新"))
