import os

release_version = "爽歪歪1.1.1"

if __name__ == '__main__':
    os.system(
        "pyinstaller -F --onefile -w -i .\\image\\XLY.ico --add-data \".\\image;image\" .\\auto_punch.py")
    os.system("del .\\dist\\" + release_version + ".exe")
    os.system("ren .\\dist\\auto_punch.exe " + release_version + ".exe")
