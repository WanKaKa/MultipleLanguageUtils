import os
import sys

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication

from app_privacy_html import main_widget


def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = main_widget.MainWidget()
    window.show()

    icon_name = resource_path(os.path.join("image", "app_icon.ico"))
    icon = QIcon()
    icon.addPixmap(QPixmap(icon_name))
    window.setWindowIcon(icon)

    sys.exit(app.exec_())
