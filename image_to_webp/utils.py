import os
import sys

from PyQt5.QtWidgets import QLineEdit


def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


def resolve_path(path):
    path = path.strip().strip('"')
    if not path:
        return ''
    if path.startswith('file:///'):
        path = path[8:]
    elif path.startswith('file://'):
        path = path[7:]
    path = os.path.normpath(path)
    if path.lower().endswith('.lnk') and os.path.isfile(path):
        try:
            import pylnk3
            lnk = pylnk3.parse(path)
            if lnk.path:
                return os.path.normpath(lnk.path)
        except Exception:
            pass
    return path


def resolve_drop_path(path, prefer_dir=False):
    path = resolve_path(path)
    if prefer_dir and path and os.path.isfile(path):
        path = os.path.dirname(path)
    return path


class DropLineEdit(QLineEdit):
    def __init__(self, prefer_dir=False, before_drop=None, parent=None):
        super().__init__(parent)
        self.prefer_dir = prefer_dir
        self.before_drop = before_drop
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if not urls:
            return
        if self.before_drop:
            self.before_drop()
        path = resolve_drop_path(urls[0].toLocalFile(), self.prefer_dir)
        if path:
            self.setText(path)
        event.acceptProposedAction()
