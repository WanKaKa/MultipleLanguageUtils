import os
import sys

from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from image_to_webp.utils import resource_path


def main():
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    icon_path = resource_path(os.path.join('ico', 'logo.ico'))
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    from image_to_webp.main_widget import MainWidget

    window = MainWidget()
    window.showMaximized()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
