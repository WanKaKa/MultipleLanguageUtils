import os

release_version = "壁纸工具1.0.1"

if __name__ == '__main__':
    os.system(
        "pyinstaller -F --onefile -w -i ..\\ico\\logo_image_config.ico --add-data \"..\\ico;ico\" .\\main_window.py")
    os.system("del .\\dist\\" + release_version + ".exe")
    os.system("ren .\\dist\\main_window.exe " + release_version + ".exe")