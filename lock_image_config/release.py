import os

release_version = "锁屏壁纸工具1.0.6"

if __name__ == '__main__':
    os.system(
        "pyinstaller -F --onefile -w -i .\\ico\\logo_image_config.ico --add-data \".\\ico;ico\" .\\run.py")
    os.system("del .\\dist\\" + release_version + ".exe")
    os.system("ren .\\dist\\run.exe " + release_version + ".exe")
