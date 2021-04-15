import re

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QBrush, QColor
from PyQt5.QtWidgets import QAbstractItemView, QTableWidgetItem

from product_multiple_language import statistics
from product_multiple_language.find_translate_copy_rename import filter_string_value_regular


def init_view(main_window):
    main_window.translate_statistics_list.itemClicked.connect(lambda: click_table_item(main_window))
    main_window.translate_statistics_list.itemDoubleClicked.connect(lambda: click_table_item_double(main_window))
    main_window.translate_statistics_click_find.clicked.connect(lambda: find_statistics_string(main_window))
    main_window.refersh_translate_statistics.clicked.connect(lambda: refresh(main_window))

    # main_window.translate_statistics_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
    # main_window.translate_statistics_list.setSelectionBehavior(QAbstractItemView.SelectRows)
    main_window.translate_statistics_list.setColumnCount(2)
    main_window.translate_statistics_list.setHorizontalHeaderLabels(['数量', '字符'])
    main_window.translate_statistics_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
    main_window.translate_statistics_list.setColumnWidth(0, 60)
    main_window.translate_statistics_list.setColumnWidth(1, 560)
    # 开始统计
    statistics_string(main_window)


def statistics_string(main_window):
    project_res_dir = main_window.input_project_path.toPlainText().strip("\n")
    if project_res_dir.startswith("file:///"):
        project_res_dir = project_res_dir[len("file:///"):]
    statistics.statistics_string(project_res_dir)
    set_statistics_string_list(main_window)


def set_statistics_string_list(main_window):
    if statistics.string_key_list:
        main_window.translate_statistics_list.setRowCount(len(statistics.string_key_list))
        for i in range(len(statistics.string_key_list)):
            set_table_widget_item(main_window, i)
    else:
        main_window.translate_statistics_list.setRowCount(0)


def set_table_widget_item(main_window, index):
    main_window.translate_statistics_list.setRowHeight(index, 40)
    key = statistics.string_key_list[index]

    item = QTableWidgetItem()
    item.setTextAlignment(Qt.AlignCenter)
    item.setFont(QFont('微软雅黑', 16))
    count = statistics.string_count_list[key]
    if count >= 20:
        item.setForeground(QBrush(QColor(85, 85, 255)))
    else:
        item.setForeground(QBrush(QColor(255, 0, 0)))
    item.setText(str(count))
    main_window.translate_statistics_list.setItem(index, 0, item)

    item = QTableWidgetItem()
    item.setFont(QFont('微软雅黑', 10))
    item.setText(statistics.string_value_list[index])
    main_window.translate_statistics_list.setItem(index, 1, item)


def click_table_item(main_window):
    print(main_window.translate_statistics_list.currentItem().text())


def click_table_item_double(main_window):
    print(main_window.translate_statistics_list.currentItem().text())


find_string = ""
find_statistics_string_index = -1


def find_statistics_string(main_window):
    global find_statistics_string_index
    global find_string
    if find_string != main_window.translate_statistics_find_string.text():
        find_statistics_string_index = -1
    find_string = main_window.translate_statistics_find_string.text()
    for index in range(len(statistics.string_value_list)):
        if find_string.lower() in re.findall(
                filter_string_value_regular, statistics.string_value_list[index])[0].lower():
            if index > find_statistics_string_index:
                find_statistics_string_index = index
                main_window.translate_statistics_list.selectRow(find_statistics_string_index)
                return
    find_statistics_string_index = -1
    for index in range(len(statistics.string_value_list)):
        if find_string.lower() in re.findall(
                filter_string_value_regular, statistics.string_value_list[index])[0].lower():
            if index > find_statistics_string_index:
                find_statistics_string_index = index
                main_window.translate_statistics_list.selectRow(find_statistics_string_index)
                return


def refresh(main_window):
    statistics_string(main_window)
