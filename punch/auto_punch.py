import os
import sys

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication

from punch import path
from punch import main_widget
from punch import utils

if __name__ == '__main__':
    path.get_cache_path()
    app = QApplication(sys.argv)

    window = main_widget.MainWidget()
    window.show()

    icon_name = utils.resource_path(os.path.join("image", "XLY.ico"))
    icon = QIcon()
    icon.addPixmap(QPixmap(icon_name))
    window.setWindowIcon(icon)

    sys.exit(app.exec_())
