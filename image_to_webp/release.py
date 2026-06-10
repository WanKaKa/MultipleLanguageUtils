import os

release_version = "PNG转WebP_1.0.0"

if __name__ == '__main__':
    os.system(
        "pyinstaller -F --onefile -w --paths .. "
        "-i .\\ico\\logo.ico "
        "--add-data \".\\assets;assets\" "
        "--add-data \".\\ico;ico\" "
        "--hidden-import PIL "
        "--hidden-import pylnk3 "
        ".\\run.py")
    os.system("del .\\dist\\" + release_version + ".exe")
    os.system("ren .\\dist\\run.exe " + release_version + ".exe")
