import sys

from PyQt5.QtWidgets import QApplication

from modify_suffix import main_view

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = main_view.MainWindow()
    main_window.show()
    sys.exit(app.exec_())
