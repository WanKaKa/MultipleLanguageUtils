import os
import re
import threading
import tkinter
import getpass

java_string_file_name_list = ["string.xml", "strings.xml"]
filter_string_key_regular = """<string name="(.+?)">"""
# 过滤的文件夹
filter_folder = ["large", "small", "dpi", "land", "port"]
language_log_name = "language_log.txt"


def copy_multiple_language():
    button1['text'] = "正在拷贝中，请勿重复点击"
    button1['bg'] = "red"

    if not os.path.exists(get_log_path()):
        os.makedirs(get_log_path())
    log_file = open(get_log_path() + language_log_name, mode='w', encoding='utf-8')

    global translate_string
    global translate_string
    translate_string = str(input1.get('0.0', 'end')).strip("\n")
    print_log(log_file, "%s\n" % translate_string)

    global translate_res_dir
    translate_res_dir = str(input2.get()).strip("\n")
    print_log(log_file, "%s\n" % translate_res_dir)

    global project_res_dir
    project_res_dir = str(input3.get()).strip("\n")
    print_log(log_file, "%s\n" % project_res_dir)

    print_log(log_file, "\n%s 解析复制开始 %s\n\n" % ("*" * 24, "*" * 24))
    add_string_key_list = analysis_equal_string(log_file)
    for root, dirs, file_paths in os.walk(translate_res_dir):
        if dirs:
            print_log(log_file, "root = %s\ndirs = %s;\nfiles = %s\n%s\n" % (root, dirs, file_paths, "*" * 50))
            for res_dir_name in dirs:
                isPassPath = False
                if "values" not in res_dir_name:
                    # 文件夹名称不包含values的文件跳过
                    isPassPath = True
                else:
                    for i in range(9):
                        if str(i) in res_dir_name:
                            # 文件夹名称包含数字0-9的文件跳过
                            isPassPath = True
                    for str_folder in filter_folder:
                        if str_folder in res_dir_name:
                            # 跳过过滤的文件夹
                            isPassPath = True
                if isPassPath:
                    continue
                if not res_dir_name == "values":
                    analysis_add_string(res_dir_name, add_string_key_list, log_file)
    print_log(log_file, "\n%s 解析复制结束 %s\n" % ("*" * 24, "*" * 24))
    log_file.close()

    button1['text'] = "拷贝"
    button1['bg'] = "green"


def analysis_equal_string(log_file):
    """
        提取相同字符的key值

        res_dir_name : 资源文件夹名称
    """
    add_string_key_list = []
    temp_read_str = ""
    for line in translate_string.split("\n"):
        temp_read_str += line
        if "resources" in temp_read_str or "</string>" in temp_read_str:
            key_list = re.findall(filter_string_key_regular, temp_read_str)
            if key_list:
                add_string_key_list.append(key_list[0])
            temp_read_str = ""
    print_log(log_file, "新增字符的KEY:\n%s\n\n%s\n" % (add_string_key_list, "*" * 50))
    return add_string_key_list


def analysis_add_string(res_dir_name, add_string_key_list, log_file):
    """
        判断项目资源文件夹中是否存在翻译字符，存在则不添加

        res_dir_name : 资源文件夹名称
        add_string_key_list : 需要添加字符的Key集合
    """
    for file_name in java_string_file_name_list:
        file_path = translate_res_dir + "\\" + res_dir_name + "\\" + file_name
        add_string = ""
        if os.path.exists(file_path):
            file = open(file_path, encoding='utf-8')
            line = file.readline()
            temp_read_str = ""
            while line:
                temp_read_str += line
                if "resources" in temp_read_str or "</string>" in temp_read_str:
                    key_list = re.findall(filter_string_key_regular, temp_read_str)
                    if key_list:
                        for key in add_string_key_list:
                            if key == key_list[0]:
                                if not string_in_project(res_dir_name, key_list[0]):
                                    add_string = add_string + "\n" + temp_read_str.strip("\n")
                                    break
                    temp_read_str = ""
                line = file.readline()
            file.close()

            add_string = add_string.strip("\n")
            if add_string:
                # 判断项目是否存在对应的语音文件夹，不存在则创建文件夹和文件
                if not os.path.exists(project_res_dir + "\\" + res_dir_name):
                    os.makedirs(project_res_dir + "\\" + res_dir_name)
                    file = open(project_res_dir + "\\" + res_dir_name + "\\strings.xml", mode='w', encoding='utf-8')
                    file.write("""<?xml version="1.0" encoding="utf-8"?>\n<resources>\n</resources>""")
                    file.close()

                add_string_to_project_res(res_dir_name, add_string)
                print_log(log_file, "语言文件夹 = %s\n新增字符:\n%s\n%s\n" % (res_dir_name, add_string, "*" * 50))
            return
    print_log(log_file, "语言文件夹 = %s\n此文件夹下没有string.xml或者strings.xml\n%s" % (res_dir_name, "*" * 50))


def string_in_project(res_dir_name, string_key):
    """
        判断字符在项目文件中是否不存在

        res_dir_name : 资源文件夹名称
        string_key : 字符名称
    """
    for file_name in java_string_file_name_list:
        file_path = project_res_dir + "\\" + res_dir_name + "\\" + file_name
        if os.path.exists(file_path):
            file = open(file_path, encoding='utf-8')
            line = file.readline()
            temp_read_str = ""
            while line:
                temp_read_str += line
                if "resources" in temp_read_str or "</string>" in temp_read_str:
                    key_list = re.findall(filter_string_key_regular, temp_read_str)
                    if key_list:
                        if key_list[0] == string_key:
                            return True
                    temp_read_str = ""
                line = file.readline()
            file.close()
    return False


def add_string_to_project_res(res_dir_name, add_str):
    """
        写入新增字符到项目字符文件中

        res_dir_name : 资源文件夹名称
        add_str : 需要插入的字符串
    """
    for file_name in java_string_file_name_list:
        file_path = project_res_dir + "\\" + res_dir_name + "\\" + file_name
        if os.path.exists(file_path):
            tmp_file_path = file_path + ".ijs"
            file = open(file_path, mode='r', encoding='utf-8')
            tmp_file = open(tmp_file_path, mode='w', encoding='utf-8')
            line = file.readline()
            while line:
                if "</resources>" in line:
                    break
                tmp_file.write(line)
                line = file.readline()
            tmp_file.write(add_str)
            tmp_file.write("\n</resources>")
            file.close()
            tmp_file.close()
            os.remove(file_path)
            os.rename(tmp_file_path, file_path)
            break


def copy_multiple_language_process():
    th = threading.Thread(target=copy_multiple_language)
    th.setDaemon(True)
    th.start()


def get_log_path():
    return 'C:\\Users\\' + getpass.getuser() + '\\Kevin\\'


def print_log(log_file, log_info):
    print(log_info)
    log_file.write(log_info)


if __name__ == '__main__':
    translate_string = ""
    translate_res_dir = ""
    project_res_dir = ""

    win = tkinter.Tk()  # 创建Windows窗口对象
    win.title("翻译拷贝程序-为便捷而生")  # 设置窗口标题
    win.geometry("1280x720")

    hint1 = """需要拷贝的字符，格式如下：<string name="i_joy_soft">IJoySoft</string>"""
    tile1 = tkinter.Label(win, text=hint1, font=('微软雅黑', 14))
    tile1.place(x=60, y=10, width=1160, height=80)

    input1 = tkinter.Text(win, font=('微软雅黑', 8))
    input1.place(x=60, y=90, width=1160, height=400)
    scroll = tkinter.Scrollbar()
    scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    scroll.config(command=input1.yview)
    input1.config(yscrollcommand=scroll.set)

    tile2 = tkinter.Label(win, text="""翻译资源文件夹路径:""", font=('微软雅黑', 14))
    tile2.place(x=60, y=490, width=1160, height=40)

    input2 = tkinter.Entry(win, font=('微软雅黑', 14))
    input2.place(x=60, y=530, width=1160, height=40)

    hint2 = r"""项目资源文件夹路径:<例如:C:\Work\ASProjects\WebBrowserNewsAS\WebBrowser\src\main\res>"""
    tile3 = tkinter.Label(win, text=hint2, font=('微软雅黑', 14))
    tile3.place(x=60, y=570, width=1160, height=40)

    input3 = tkinter.Entry(win, font=('微软雅黑', 14))
    input3.place(x=60, y=610, width=1160, height=40)

    button1 = tkinter.Button(win, text="拷贝", bg="green", fg="white", font=('微软雅黑', 14))
    button1['command'] = copy_multiple_language_process
    button1.place(x=60, y=665, width=300, height=40)

    button2 = tkinter.Button(win, text="删除", bg="red", fg="white", font=('微软雅黑', 14))
    button2.place(x=920, y=665, width=300, height=40)

    if os.path.exists(get_log_path() + language_log_name):
        read_log = open(get_log_path() + language_log_name, mode='r', encoding='utf-8')
        line_log = read_log.readline()
        while line_log:
            if not re.findall(filter_string_key_regular, line_log):
                break
            input1.insert("insert", line_log)
            line_log = read_log.readline()
        input2.insert("insert", line_log.replace("\n", ""))
        input3.insert("insert", read_log.readline().replace("\n", ""))
        read_log.close()
    win.mainloop()
