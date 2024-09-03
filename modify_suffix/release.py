import os

release_version = "UI脚本1.0.3"

if __name__ == '__main__':
    os.system(
        "pyinstaller -F --onefile -w -i .\\image\\fast.ico --add-data \".\\image;image\" .\\run.py")
    os.system("del .\\dist\\" + release_version + ".exe")
    os.system("ren .\\dist\\run.exe " + release_version + ".exe")
