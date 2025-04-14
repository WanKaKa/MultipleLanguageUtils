import os

release_version = "TXT转HTML_1.0.3"

if __name__ == '__main__':
    os.system(
        "pyinstaller -F --onefile -w -i .\\image\\app_icon.ico --add-data \".\\image;image\" .\\run_aph.py")
    os.system("del .\\dist\\" + release_version + ".exe")
    os.system("ren .\\dist\\run_aph.exe " + release_version + ".exe")
