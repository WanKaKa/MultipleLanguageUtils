# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1155, 818)
        Form.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.formLayout = QtWidgets.QFormLayout(Form)
        self.formLayout.setObjectName("formLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setMinimumSize(QtCore.QSize(0, 40))
        self.label.setMaximumSize(QtCore.QSize(16777215, 40))
        self.label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 12pt \"微软雅黑\";")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.input_string = QtWidgets.QTextEdit(Form)
        self.input_string.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 10pt \"微软雅黑\";")
        self.input_string.setObjectName("input_string")
        self.verticalLayout.addWidget(self.input_string)
        self.frame_3 = QtWidgets.QFrame(Form)
        self.frame_3.setMinimumSize(QtCore.QSize(0, 40))
        self.frame_3.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.label_2 = QtWidgets.QLabel(self.frame_3)
        self.label_2.setGeometry(QtCore.QRect(0, 0, 180, 40))
        self.label_2.setMinimumSize(QtCore.QSize(0, 40))
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 40))
        self.label_2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 12pt \"微软雅黑\";")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.old_translate_path = QtWidgets.QLabel(self.frame_3)
        self.old_translate_path.setGeometry(QtCore.QRect(180, 0, 805, 40))
        self.old_translate_path.setStyleSheet("color: rgb(85, 85, 255);\n"
"font: 12pt \"微软雅黑\";")
        self.old_translate_path.setText("")
        self.old_translate_path.setAlignment(QtCore.Qt.AlignCenter)
        self.old_translate_path.setObjectName("old_translate_path")
        self.copy_translate_path = QtWidgets.QPushButton(self.frame_3)
        self.copy_translate_path.setGeometry(QtCore.QRect(985, 5, 75, 30))
        self.copy_translate_path.setStyleSheet("background-color: rgb(85, 85, 255);\n"
"font: 12pt \"微软雅黑\";\n"
"color: rgb(255, 255, 255);")
        self.copy_translate_path.setObjectName("copy_translate_path")
        self.verticalLayout.addWidget(self.frame_3)
        self.input_translate_path = QtWidgets.QTextEdit(Form)
        self.input_translate_path.setMinimumSize(QtCore.QSize(0, 60))
        self.input_translate_path.setMaximumSize(QtCore.QSize(16777215, 60))
        self.input_translate_path.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.input_translate_path.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(85, 85, 255);\n"
"font: 12pt \"微软雅黑\";")
        self.input_translate_path.setObjectName("input_translate_path")
        self.verticalLayout.addWidget(self.input_translate_path)
        self.frame_4 = QtWidgets.QFrame(Form)
        self.frame_4.setMinimumSize(QtCore.QSize(0, 40))
        self.frame_4.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.label_3 = QtWidgets.QLabel(self.frame_4)
        self.label_3.setGeometry(QtCore.QRect(0, 0, 180, 40))
        self.label_3.setMinimumSize(QtCore.QSize(0, 40))
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 40))
        self.label_3.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 12pt \"微软雅黑\";")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.old_project_path = QtWidgets.QLabel(self.frame_4)
        self.old_project_path.setGeometry(QtCore.QRect(180, 0, 805, 40))
        self.old_project_path.setStyleSheet("color: rgb(85, 85, 255);\n"
"font: 12pt \"微软雅黑\";")
        self.old_project_path.setText("")
        self.old_project_path.setAlignment(QtCore.Qt.AlignCenter)
        self.old_project_path.setObjectName("old_project_path")
        self.copy_project_path = QtWidgets.QPushButton(self.frame_4)
        self.copy_project_path.setGeometry(QtCore.QRect(985, 5, 75, 30))
        self.copy_project_path.setStyleSheet("background-color: rgb(85, 85, 255);\n"
"font: 12pt \"微软雅黑\";\n"
"color: rgb(255, 255, 255);")
        self.copy_project_path.setObjectName("copy_project_path")
        self.verticalLayout.addWidget(self.frame_4)
        self.input_project_path = QtWidgets.QTextEdit(Form)
        self.input_project_path.setMinimumSize(QtCore.QSize(0, 60))
        self.input_project_path.setMaximumSize(QtCore.QSize(16777215, 60))
        self.input_project_path.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(85, 85, 255);\n"
"font: 12pt \"微软雅黑\";")
        self.input_project_path.setObjectName("input_project_path")
        self.verticalLayout.addWidget(self.input_project_path)
        self.frame_5 = QtWidgets.QFrame(Form)
        self.frame_5.setMinimumSize(QtCore.QSize(0, 60))
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.label_4 = QtWidgets.QLabel(self.frame_5)
        self.label_4.setGeometry(QtCore.QRect(0, 0, 180, 60))
        self.label_4.setMinimumSize(QtCore.QSize(0, 60))
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 40))
        self.label_4.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 12pt \"微软雅黑\";")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.ignore_language_01 = QtWidgets.QCheckBox(self.frame_5)
        self.ignore_language_01.setGeometry(QtCore.QRect(180, 0, 150, 30))
        self.ignore_language_01.setStyleSheet("font: 12pt \"微软雅黑\";")
        self.ignore_language_01.setObjectName("ignore_language_01")
        self.ignore_language_02 = QtWidgets.QCheckBox(self.frame_5)
        self.ignore_language_02.setGeometry(QtCore.QRect(330, 0, 150, 30))
        self.ignore_language_02.setStyleSheet("font: 12pt \"微软雅黑\";")
        self.ignore_language_02.setObjectName("ignore_language_02")
        self.ignore_language_03 = QtWidgets.QCheckBox(self.frame_5)
        self.ignore_language_03.setGeometry(QtCore.QRect(480, 0, 150, 30))
        self.ignore_language_03.setStyleSheet("font: 12pt \"微软雅黑\";")
        self.ignore_language_03.setObjectName("ignore_language_03")
        self.ignore_language_04 = QtWidgets.QCheckBox(self.frame_5)
        self.ignore_language_04.setGeometry(QtCore.QRect(630, 0, 150, 30))
        self.ignore_language_04.setStyleSheet("font: 12pt \"微软雅黑\";")
        self.ignore_language_04.setObjectName("ignore_language_04")
        self.ignore_language_11 = QtWidgets.QCheckBox(self.frame_5)
        self.ignore_language_11.setGeometry(QtCore.QRect(180, 30, 150, 30))
        self.ignore_language_11.setStyleSheet("font: 12pt \"微软雅黑\";")
        self.ignore_language_11.setObjectName("ignore_language_11")
        self.ignore_language_12 = QtWidgets.QCheckBox(self.frame_5)
        self.ignore_language_12.setGeometry(QtCore.QRect(330, 30, 150, 30))
        self.ignore_language_12.setStyleSheet("font: 12pt \"微软雅黑\";")
        self.ignore_language_12.setObjectName("ignore_language_12")
        self.ignore_language_13 = QtWidgets.QCheckBox(self.frame_5)
        self.ignore_language_13.setGeometry(QtCore.QRect(480, 30, 150, 30))
        self.ignore_language_13.setStyleSheet("font: 12pt \"微软雅黑\";")
        self.ignore_language_13.setObjectName("ignore_language_13")
        self.ignore_language_14 = QtWidgets.QCheckBox(self.frame_5)
        self.ignore_language_14.setGeometry(QtCore.QRect(630, 30, 150, 30))
        self.ignore_language_14.setStyleSheet("font: 12pt \"微软雅黑\";")
        self.ignore_language_14.setObjectName("ignore_language_14")
        self.ignore_language_select_all = QtWidgets.QPushButton(self.frame_5)
        self.ignore_language_select_all.setGeometry(QtCore.QRect(985, 15, 75, 30))
        self.ignore_language_select_all.setStyleSheet("background-color: rgb(85, 85, 255);\n"
"font: 12pt \"微软雅黑\";\n"
"color: rgb(255, 255, 255);")
        self.ignore_language_select_all.setObjectName("ignore_language_select_all")
        self.verticalLayout.addWidget(self.frame_5)
        self.ignore_language_text = QtWidgets.QTextEdit(Form)
        self.ignore_language_text.setMaximumSize(QtCore.QSize(16777215, 60))
        self.ignore_language_text.setStyleSheet("font: 12pt \"微软雅黑\";")
        self.ignore_language_text.setObjectName("ignore_language_text")
        self.verticalLayout.addWidget(self.ignore_language_text)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_2 = QtWidgets.QFrame(Form)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout.addWidget(self.frame_2)
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setMinimumSize(QtCore.QSize(540, 60))
        self.frame.setMaximumSize(QtCore.QSize(540, 60))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.copy_string = QtWidgets.QPushButton(self.frame)
        self.copy_string.setGeometry(QtCore.QRect(0, 10, 120, 40))
        self.copy_string.setStyleSheet("background-color: rgb(85, 85, 255);\n"
"font: 12pt \"微软雅黑\";\n"
"color: rgb(255, 255, 255);")
        self.copy_string.setObjectName("copy_string")
        self.delete_string = QtWidgets.QPushButton(self.frame)
        self.delete_string.setGeometry(QtCore.QRect(140, 10, 120, 40))
        self.delete_string.setStyleSheet("background-color: rgb(255, 85, 127);\n"
"font: 12pt \"微软雅黑\";\n"
"color: rgb(255, 255, 255);")
        self.delete_string.setObjectName("delete_string")
        self.open_copy_logo = QtWidgets.QPushButton(self.frame)
        self.open_copy_logo.setGeometry(QtCore.QRect(280, 10, 120, 40))
        self.open_copy_logo.setStyleSheet("background-color: rgb(85, 85, 255);\n"
"font: 12pt \"微软雅黑\";\n"
"color: rgb(255, 255, 255);")
        self.open_copy_logo.setObjectName("open_copy_logo")
        self.open_delete_log = QtWidgets.QPushButton(self.frame)
        self.open_delete_log.setGeometry(QtCore.QRect(420, 10, 120, 40))
        self.open_delete_log.setStyleSheet("background-color: rgb(85, 85, 255);\n"
"font: 12pt \"微软雅黑\";\n"
"color: rgb(255, 255, 255);")
        self.open_delete_log.setObjectName("open_delete_log")
        self.horizontalLayout.addWidget(self.frame)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.SpanningRole, self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "需要拷贝的字符，格式如下：<string name=\"i_joy_soft\">IJoySoft</string>"))
        self.label_2.setText(_translate("Form", "翻译资源文件夹路径:"))
        self.copy_translate_path.setText(_translate("Form", "使用"))
        self.label_3.setText(_translate("Form", "项目资源文件夹路径:"))
        self.copy_project_path.setText(_translate("Form", "使用"))
        self.label_4.setText(_translate("Form", "忽略的语言:"))
        self.ignore_language_01.setText(_translate("Form", "CheckBox"))
        self.ignore_language_02.setText(_translate("Form", "CheckBox"))
        self.ignore_language_03.setText(_translate("Form", "CheckBox"))
        self.ignore_language_04.setText(_translate("Form", "CheckBox"))
        self.ignore_language_11.setText(_translate("Form", "CheckBox"))
        self.ignore_language_12.setText(_translate("Form", "CheckBox"))
        self.ignore_language_13.setText(_translate("Form", "CheckBox"))
        self.ignore_language_14.setText(_translate("Form", "CheckBox"))
        self.ignore_language_select_all.setText(_translate("Form", "(非)全选"))
        self.copy_string.setText(_translate("Form", "拷贝"))
        self.delete_string.setText(_translate("Form", "删除"))
        self.open_copy_logo.setText(_translate("Form", "Log-拷贝"))
        self.open_delete_log.setText(_translate("Form", "Log-删除"))
