import os
import sys

from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from modify_suffix.utils import resource_path


def main():
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    icon_path = resource_path(os.path.join('image', 'fast.ico'))
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    from modify_suffix import main_view

    main_window = main_view.MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
