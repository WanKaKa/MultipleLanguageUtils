import os
import re
import threading
import tkinter
import tkinter.messagebox
from multiple_language import kevin_utils
from multiple_language import multiple_language_utils
from multiple_language import delete_res_string


def request_copy_multiple_language():
    if tkinter.messagebox.askokcancel('提示', '执行翻译操作吗'):
        copy_multiple_language_process()


def copy_multiple_language_process():
    th = threading.Thread(target=copy_multiple_language)
    th.setDaemon(True)
    th.start()


def copy_multiple_language():
    button1['text'] = "正在拷贝中，请勿重复点击"
    button1['bg'] = "red"
    multiple_language_utils.copy_multiple_language(
        str(input1.get('0.0', 'end')).strip("\n"), str(input2.get()).strip("\n"), str(input3.get()).strip("\n"))
    button1['text'] = "拷贝"
    button1['bg'] = "green"


def request_delete_android_values_string():
    if tkinter.messagebox.askokcancel('提示', '执行删除操作吗'):
        delete_android_values_string_process()


def delete_android_values_string_process():
    input_strings = str(input1.get('0.0', 'end')).strip("\n")
    project_dir = str(input3.get()).strip("\n")
    th = threading.Thread(
        target=lambda: delete_res_string.delete_android_values_string(project_dir, input_strings, button2))
    th.setDaemon(True)
    th.start()


if __name__ == '__main__':
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
    button1['command'] = request_copy_multiple_language
    button1.place(x=60, y=665, width=300, height=40)

    button2 = tkinter.Button(win, text="删除", bg="red", fg="white", font=('微软雅黑', 14))

    button2['command'] = request_delete_android_values_string
    button2.place(x=920, y=665, width=300, height=40)

    if os.path.exists(kevin_utils.get_log_path() + kevin_utils.language_log_name):
        read_log = open(kevin_utils.get_log_path() + kevin_utils.language_log_name,
                        mode='r', encoding='utf-8')
        line_log = read_log.readline()
        while line_log:
            if (not re.findall(kevin_utils.filter_string_key_regular, line_log)) \
                    and (not re.findall(kevin_utils.filter_explain_string_key_regular, line_log)) \
                    and ("</string>" not in line_log) \
                    and (line_log.replace("\n", "") != "") \
                    and ("\\res" in line_log):
                break
            input1.insert("insert", line_log)
            line_log = read_log.readline()
        input2.insert("insert", line_log.replace("\n", ""))
        input3.insert("insert", read_log.readline().replace("\n", ""))
        read_log.close()
    win.mainloop()
