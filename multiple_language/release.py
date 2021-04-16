import os

release_version = "多语言拷贝脚本1.2.0"

os.system(
    "pyinstaller -F --onefile -w -i .\\ico\\logo_multiple_language.ico --add-data \".\\ico;ico\" .\\main_window.py")
os.system("del .\\dist\\" + release_version + ".exe")
os.system("ren .\\dist\\main_window.exe " + release_version + ".exe")
