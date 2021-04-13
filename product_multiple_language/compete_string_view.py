import os
import re

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QBrush, QColor
from PyQt5.QtWidgets import QAbstractItemView, QTableWidgetItem, QFileDialog

import multiple_language.database
import product_multiple_language.main_window

from product_multiple_language import statistics
from product_multiple_language.find_translate_copy_rename import filter_string_value_regular


def init_view(main_window: product_multiple_language.main_window.MainWindow):
    main_window.compete_string_click_select_dir.clicked.connect(lambda: set_compete_string_dir(main_window))
    main_window.compete_string_list.itemClicked.connect(lambda: click_table_item(main_window))
    main_window.compete_string_list.itemDoubleClicked.connect(lambda: click_table_item_double(main_window))
    main_window.compete_string_click_find.clicked.connect(lambda: find_compete_string(main_window))
    main_window.compete_string_click_rename.clicked.connect(lambda: rename(main_window))
    main_window.compete_string_click_refresh.clicked.connect(lambda: refresh(main_window))

    main_window.compete_string_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
    main_window.compete_string_list.setSelectionBehavior(QAbstractItemView.SelectRows)
    main_window.compete_string_list.setColumnCount(3)
    main_window.compete_string_list.setHorizontalHeaderLabels(['字符Key', '字符', '数量'])
    main_window.compete_string_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
    main_window.compete_string_list.setColumnWidth(0, 120)
    main_window.compete_string_list.setColumnWidth(1, 440)
    main_window.compete_string_list.setColumnWidth(2, 40)

    # data = multiple_language.database.get_json_data()
    # if data and "compete_string_dir" in data:
    #     main_window.compete_string_dir.setText(data["compete_string_dir"])
    #     statistics.statistics_string(data["compete_string_dir"])
    #     set_compete_string_list(main_window)


def set_compete_string_list(main_window: product_multiple_language.main_window.MainWindow):
    if statistics.string_key_list:
        main_window.compete_string_list.setRowCount(len(statistics.string_key_list))
        for i in range(len(statistics.string_key_list)):
            set_table_widget_item(main_window, i)
    else:
        main_window.compete_string_list.setRowCount(0)


def set_table_widget_item(main_window: product_multiple_language.main_window.MainWindow, index):
    main_window.compete_string_list.setRowHeight(index, 20)

    item = QTableWidgetItem()
    item.setFont(QFont('微软雅黑', 8))
    key = statistics.string_key_list[index]
    item.setText(statistics.string_key_list[index])
    main_window.compete_string_list.setItem(index, 0, item)

    item = QTableWidgetItem()
    item.setFont(QFont('微软雅黑', 12))
    item.setForeground(QBrush(QColor(85, 85, 255)))
    item.setText(re.findall(filter_string_value_regular, statistics.string_value_list[index])[0])
    main_window.compete_string_list.setItem(index, 1, item)

    item = QTableWidgetItem()
    item.setTextAlignment(Qt.AlignCenter)
    item.setFont(QFont('微软雅黑', 8))
    if key in statistics.string_count_list:
        item.setText(str(statistics.string_count_list[key]))
    main_window.compete_string_list.setItem(index, 2, item)


def set_compete_string_dir(main_window: product_multiple_language.main_window.MainWindow):
    data = multiple_language.database.get_json_data()
    if data and "compete_string_dir" in data:
        dir_path = QFileDialog.getExistingDirectory(main_window, "选取文件夹", os.path.dirname(data["compete_string_dir"]))
    else:
        dir_path = QFileDialog.getExistingDirectory(main_window, "选取文件夹", os.getcwd())
    if dir_path:
        multiple_language.database.set_json_data({"compete_string_dir": dir_path})
        main_window.compete_string_dir.setText(dir_path)
        statistics.statistics_string(dir_path)
        set_compete_string_list(main_window)


def click_table_item(main_window: product_multiple_language.main_window.MainWindow):
    key = statistics.string_key_list[main_window.compete_string_list.currentItem().row()]
    main_window.compete_string_need_rename.setText(key)


def click_table_item_double(main_window: product_multiple_language.main_window.MainWindow):
    print(main_window.compete_string_list.currentItem().text())


find_string = ""
find_compete_string_index = -1


def find_compete_string(main_window: product_multiple_language.main_window.MainWindow):
    global find_compete_string_index
    global find_string
    if find_string != main_window.compete_string_find_string.text():
        find_compete_string_index = -1
    find_string = main_window.compete_string_find_string.text()
    for index in range(len(statistics.string_value_list)):
        if find_string.lower() in re.findall(
                filter_string_value_regular, statistics.string_value_list[index])[0].lower():
            if index > find_compete_string_index:
                find_compete_string_index = index
                main_window.compete_string_list.selectRow(find_compete_string_index)
                return
    find_compete_string_index = -1
    for index in range(len(statistics.string_value_list)):
        if find_string.lower() in re.findall(
                filter_string_value_regular, statistics.string_value_list[index])[0].lower():
            if index > find_compete_string_index:
                find_compete_string_index = index
                main_window.compete_string_list.selectRow(find_compete_string_index)
                return


def rename(main_window: product_multiple_language.main_window.MainWindow):
    compete_string_dir = main_window.compete_string_dir.text()
    if compete_string_dir:
        product_multiple_language.find_translate_copy_rename.translate_reference_key_list.clear()
        product_multiple_language.find_translate_copy_rename.translate_project_key_list.clear()

        string1 = main_window.compete_string_need_rename.text()
        if "<string" in string1 and "</string>" in string1:
            product_multiple_language.find_translate_copy_rename.translate_reference_key_list.append(
                re.findall(filter_string_value_regular, string1)[0])
        else:
            product_multiple_language.find_translate_copy_rename.translate_reference_key_list.append(string1)

        string2 = main_window.project_string_name.text()
        if "<string" in string2 and "</string>" in string2:
            product_multiple_language.find_translate_copy_rename.translate_project_key_list.append(
                re.findall(filter_string_value_regular, string2)[0])
        else:
            product_multiple_language.find_translate_copy_rename.translate_project_key_list.append(string2)
        product_multiple_language.find_translate_copy_rename.translate_res_delete_string(compete_string_dir)
        product_multiple_language.find_translate_copy_rename.translate_res_rename_string(compete_string_dir)
        main_window.compete_string_need_rename.setText("")
        main_window.project_string_name.setText("")
        refresh(main_window)


def refresh(main_window: product_multiple_language.main_window.MainWindow):
    compete_string_dir = main_window.compete_string_dir.text()
    if compete_string_dir:
        statistics.statistics_string(compete_string_dir)
        set_compete_string_list(main_window)
