# -*- coding:utf-8 -*-
import os
import shutil

# 项目详情
# 项目名、项目路径、项目主模块名、包名
projects_details = [
    ["WebBrowserAS", "C:\\Work\\ASProjects\\", "\\WebBrowser", "fast.explorer.web.browser"],
    ["WebBrowserNewsAS", "C:\\Work\\ASProjects\\", "\\WebBrowser", "fast.private.secure.browser"],
    ["WebBrowserQQAS", "C:\\Work\\ASProjects\\", "\\WebBrowser", "net.fast.web.browser"],
    ["WebBrowserSearchAS", "C:\\Work\\ASProjects\\", "\\WebBrowser", "org.easyweb.browser"],
    ["WebBrowserTabAS", "C:\\Work\\ASProjects\\", "\\WebBrowser", "com.explore.web.browser"],
    ["WebBrowserSlideAS", "C:\\Work\\ASProjects\\", "\\WebBrowser", "secure.explorer.web.browser"],
    ["WebBrowserThemeAS", "C:\\Work\\ASProjects\\", "\\WebBrowser", "privacy.explorer.fast.safe.browser"],
    ["LockScreenGridAS", "C:\\Work\\ASProjects\\", "\\app", "tool.keypad.locker.lockscreen"],
    ["LockScreenTabAS", "C:\\Work\\ASProjects\\", "\\app", "keypad.locker.wallpaper.lockscreen"],
    ["BarcodeTabAS", "C:\\Work\\ASProjects\\", "\\BarcodeTab", "tool.qr.scanner.barcode.scanner"],
    ["BarcodeScannerAs", "C:\\Work\\ASProjects\\", "\\BarcodeScanner", "tool.scanner.qrscan.barcodescan"],
    ["NoteAS", "C:\\Work\\ASProjects\\", "\\Note", "com.task.notes"],
    ["NotebookAS", "C:\\Work\\ASProjects\\", "\\NoteBook", "tool.notepad.notes.notebooks"],
    ["WeatherAccurate", "C:\\Work\\ASProjects\\", "\\WeatherForecast", "accurate.local.weather.forecast.channel"],
    ["WeatherForecastAS", "C:\\Work\\ASProjects\\", "\\WeatherForecast", "weather.forecast.live.weather"],
    ["WeatherForecastBM", "C:\\Work\\ASProjects\\", "\\WeatherForecast", "weather.local.weather.forecast.channel"],
    ["WeatherForecastGrid", "C:\\Work\\ASProjects\\", "\\WeatherForecast", "local.weather.forecast.pro"],
    ["WeatherForecastBlack", "C:\\Work\\ASProjects\\", "\\WeatherForecast", "weather.radar.real.weather.forecast"],
    ["LauncherIOS", "C:\\Work\\ASProjects\\", "\\app", "theme.wallpaper.smart.launcher"],
    ["AdvertLibraryExampleAS", "C:\\Work\\ASProjects\\", "\\app", "com.ijoysoft.advert"],
    ["ScreenRecorderAS", "C:\\Work\\ASProjects\\", "\\app", "tool.video.recorder.screenrecorder"],
    ["ScreenRecorderTheme", "C:\\Work\\ASProjects\\", "\\app", "smart.video.recorder.screenrecorder"],
    ["ScreenRecorderTabAS", "C:\\Work\\ASProjects\\", "\\app", "tool.video.screen.recorder"],
]
# 安装成功后，拷贝apk和txt的路径
copy_files_dir = "C:/Users/DELL/Desktop/release/"


def init_main_menu():
    size = len(str(len(projects_details)))
    menu = "\n" * 3 + "选择项目".center(35, "*") + "\n"
    for project in projects_details:
        menu += str(projects_details.index(project)).rjust(size) + ": " + "\033[0;32;40m%s\033[0m" % project[0] + "\n"
    menu = menu + "E".rjust(size) + ": \033[0;31;40m%s\033[0m\n" % "退出程序" + "".center(40, "*")
    return menu


def init_sub_menu():
    menu = "\n" * 3 + "选择操作".center(36, "*") + "\n"
    menu += "0: \033[0;32;40m卸载\033[0m" + "\n"
    menu += "1: \033[0;32;40m安装\033[0m" + "\n"
    menu += "2: \033[0;32;40m返回\033[0m" + "\n"
    menu += "E: \033[0;31;40m退出程序\033[0m" + "\n"
    menu += "".center(40, "*")
    return menu


def input_digit():
    index = input(">>>")
    if index.isdigit():
        return int(index)
    else:
        return None


def uninstall_apk(project_index):
    if 0 <= project_index < len(projects_details):
        os.system("adb uninstall " + projects_details[project_index][3])


def install_apk(project_index, apk_index):
    apk_files = []
    if 0 <= project_index < len(projects_details):
        project = projects_details[project_index]
        apk_dir = project[1] + project[0] + project[2] + "\\build\\outputs\\apk\\"
        # 获取apk
        for root, dirs, files in os.walk(apk_dir):
            for file in files:
                path = os.path.join(root, file)
                ext = os.path.splitext(path)[1]
                if ext in [".apk"]:
                    apk_files.append(path)
        # 未选择apk的index时，显示菜单
        if apk_index is None:
            menu = "\n" * 3 + "选择安装的Apk文件".center(33, "*") + "\n"
            for path in apk_files:
                index = str(apk_files.index(path)).rjust(len(str(len(apk_files))))
                detail = os.path.basename(path) + " " + str(os.path.getsize(path) / 1000) + "Kb"
                menu += index + ". " + "\033[0;32;40m%s\033[0m" % detail + "\n"
            menu += "".center(40, "*")
            print(menu)
            apk_index = input_digit()

        if apk_index is not None:
            if 0 <= apk_index < len(apk_files):
                os.system("adb install " + apk_files[apk_index])
                # 拷贝文件
                file_name = os.path.splitext(os.path.split(apk_files[apk_index])[1])[0]
                if input(">>>是否拷贝Apk到发布文件夹(Y/N): ").upper() == "Y":
                    for root, dirs, files in os.walk(apk_dir):
                        for file in files:
                            if file_name in file:
                                copy_dir = copy_files_dir + project[0] + "/"
                                if not os.path.exists(copy_dir):
                                    os.makedirs(copy_dir)
                                shutil.copy(os.path.join(root, file), copy_dir)
                                print("拷贝成功: " + "\033[0;32;40m%s\033[0m" % file)
                else:
                    print("\033[0;31;40m取消拷贝\033[0m")
            else:
                print("\033[0;31;40mAPK不存在\033[0m")
        else:
            print("\033[0;31;40m未选择APK\033[0m")


def kevin():
    main_menu = init_main_menu()
    sub_menu = init_sub_menu()
    while True:
        operation_index = None
        apk_index = None

        # 显示主菜单
        print(main_menu)
        while True:
            main_input = input(">>>")
            if main_input.isdigit():
                # 输入为数字时
                if 0 <= int(main_input) < len(projects_details):
                    project_index = int(main_input)
                    break
            elif "E" in main_input.upper():
                # 输入E退出
                exit()
            else:
                # 输入不为数字时，可能是数字数组，以.分隔
                index_list = main_input.split(".")
                if len(index_list) == 2 or len(index_list) == 3:
                    if index_list[0].isdigit() and index_list[1].isdigit():
                        if 0 <= int(index_list[0]) < len(projects_details) and 0 <= int(index_list[1]) < 3:
                            # 数组前两个为数字且范围正确视为输入有效
                            project_index = int(index_list[0])
                            operation_index = int(index_list[1])
                            if len(index_list) == 3:
                                if index_list[2].isdigit():
                                    # 如果数组大小为3且第三个字符也为数字，则为apk_index赋值
                                    apk_index = int(index_list[2])
                            break
        # 如果次级菜单index没有输入，则显示次级菜单
        if operation_index is None:
            print(sub_menu)
            while True:
                sub_input = input(">>>")
                if sub_input.isdigit():
                    if 0 <= int(sub_input) < 3:
                        operation_index = int(sub_input)
                        break
                elif "E" in sub_input.upper():
                    exit()

        if operation_index == 0:
            uninstall_apk(project_index)
            continue
        if operation_index == 1:
            install_apk(project_index, apk_index)


if __name__ == '__main__':
    kevin()
