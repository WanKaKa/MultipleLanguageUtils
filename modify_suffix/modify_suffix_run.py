import os
import tkinter
import getpass
import shutil

log_file_name = "modify_suffix.log"


def start_modify_suffix():
    log_file = open(get_user_path() + log_file_name, mode='w', encoding='utf-8')
    global target
    target = str(input1.get()).strip("\n")
    log_file.write("%s\n" % target)
    global replacement
    replacement = str(input2.get()).strip("\n")
    log_file.write("%s\n" % replacement)
    global path
    path = str(input3.get()).strip("\n")
    log_file.write("%s\n" % path)

    modify_suffix(path, log_file)
    log_file.close()


def modify_suffix(dir_path, log_file):
    file_list = os.listdir(dir_path)
    for file in file_list:
        old_file = os.path.join(dir_path, file)
        if os.path.isdir(old_file):
            modify_suffix(old_file, log_file)
        else:
            if target == ".":
                portion = os.path.splitext(file)
                if not portion[1]:
                    new_suf = os.path.join(dir_path, file + replacement)
                else:
                    new_suf = old_file
            else:
                new_suf = old_file.replace(target, replacement)
            log_file.write("原始文件：%s\n" % old_file)
            print("原始文件：%s\n" % old_file)
            log_file.write("修改文件：%s\n" % new_suf)
            print("修改文件：%s\n" % new_suf)
            shutil.move(old_file, new_suf)


def start_bandizip():
    log_file = open(get_user_path() + log_file_name, mode='w', encoding='utf-8')
    global target
    target = str(input1.get()).strip("\n")
    log_file.write("%s\n" % target)
    global replacement
    replacement = str(input2.get()).strip("\n")
    log_file.write("%s\n" % replacement)
    global path
    path = str(input3.get()).strip("\n")
    log_file.write("%s\n" % path)

    bandizip(path, log_file)
    log_file.close()


def bandizip(dir_path, log_file):
    file_list = os.listdir(dir_path)
    for file in file_list:
        old_file = os.path.join(dir_path, file)
        if os.path.isdir(old_file):
            value = "bandizip.exe c " + old_file + "/" + file + ".zip " + old_file
            print(value)
            os.system(value)


def start_delete():
    log_file = open(get_user_path() + log_file_name, mode='w', encoding='utf-8')
    global target
    target = str(input1.get()).strip("\n")
    log_file.write("%s\n" % target)
    global replacement
    replacement = str(input2.get()).strip("\n")
    log_file.write("%s\n" % replacement)
    global path
    path = str(input3.get()).strip("\n")
    log_file.write("%s\n" % path)

    delete(path, log_file)
    log_file.close()


def delete(dir_path, log_file):
    file_list = os.listdir(dir_path)
    for file in file_list:
        old_file = os.path.join(dir_path, file)
        if os.path.isdir(old_file):
            file_list_2 = os.listdir(old_file)
            for file_2 in file_list_2:
                old_file_2 = os.path.join(old_file, file_2)
                if not os.path.isdir(old_file_2):
                    if "frame" in file_2:
                        os.remove(old_file_2)


def get_user_path():
    return "C:\\IJoySoft\\Kevin\\ModifySuffix\\"


if __name__ == '__main__':
    target = ""
    replacement = ""
    path = ""

    win = tkinter.Tk()  # 创建Windows窗口对象
    win.title("后缀名修改脚本-为便捷而生")  # 设置窗口标题
    win.geometry("960x450")

    tile1 = tkinter.Label(win, text="""旧的后缀名""", font=('Consolas', 16))
    tile1.place(x=60, y=50, width=840, height=20)
    input1 = tkinter.Entry(win, font=('Consolas', 16))
    input1.place(x=60, y=70, width=840, height=40)

    tile2 = tkinter.Label(win, text="""新的后缀名""", font=('Consolas', 16))
    tile2.place(x=60, y=160, width=840, height=20)
    input2 = tkinter.Entry(win, font=('Consolas', 16))
    input2.place(x=60, y=180, width=840, height=40)

    tile3 = tkinter.Label(win, text="""文件夹路径""", font=('Consolas', 16))
    tile3.place(x=60, y=270, width=840, height=20)
    input3 = tkinter.Entry(win, font=('Consolas', 16))
    input3.place(x=60, y=290, width=840, height=40)

    button = tkinter.Button(win, text="修改", fg="white", bg="green", font=('Consolas', 16), command=start_modify_suffix)
    button.place(x=100, y=380, width=240, height=40)

    button = tkinter.Button(win, text="压缩", fg="white", bg="green", font=('Consolas', 16), command=start_bandizip)
    button.place(x=400, y=380, width=240, height=40)

    button = tkinter.Button(win, text="删除", fg="white", bg="green", font=('Consolas', 16), command=start_delete)
    button.place(x=700, y=380, width=240, height=40)

    if os.path.exists(get_user_path() + log_file_name):
        read_log = open(get_user_path() + log_file_name, mode='r', encoding='utf-8')
        input1.insert("insert", read_log.readline().replace("\n", ""))
        input2.insert("insert", read_log.readline().replace("\n", ""))
        input3.insert("insert", read_log.readline().replace("\n", ""))
        read_log.close()
    win.mainloop()
