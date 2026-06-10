from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QLabel, QProgressBar, QVBoxLayout

from modify_suffix.styles import get_zip_busy_stylesheet


class ZipBusyDialog(QDialog):
    _SPINNER_FRAMES = ('⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏')

    def __init__(self, action_text, total, parent=None):
        super().__init__(parent)
        self.setObjectName('zipBusyDialog')
        self.setWindowTitle(f'{action_text}中')
        self.setWindowModality(Qt.WindowModal)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)
        self.setFixedWidth(400)
        self.setStyleSheet(get_zip_busy_stylesheet())

        self._spin_index = 0

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(16)

        top_row = QHBoxLayout()
        top_row.setSpacing(12)

        self._spinner_label = QLabel(self._SPINNER_FRAMES[0])
        self._spinner_label.setObjectName('zipSpinner')
        self._spinner_label.setAlignment(Qt.AlignCenter)
        self._spinner_label.setFixedSize(40, 40)

        self._title_label = QLabel(f'正在{action_text}...')
        self._title_label.setObjectName('zipBusyTitle')

        top_row.addWidget(self._spinner_label)
        top_row.addWidget(self._title_label, 1)
        layout.addLayout(top_row)

        self._progress_bar = QProgressBar()
        self._progress_bar.setObjectName('zipBusyProgress')
        self._progress_bar.setRange(0, max(total, 1))
        self._progress_bar.setValue(0)
        self._progress_bar.setTextVisible(True)
        self._progress_bar.setFormat('%v / %m')
        layout.addWidget(self._progress_bar)

        self._detail_label = QLabel('')
        self._detail_label.setObjectName('zipBusyDetail')
        self._detail_label.setAlignment(Qt.AlignCenter)
        self._detail_label.setWordWrap(True)
        layout.addWidget(self._detail_label)

        self._spin_timer = QTimer(self)
        self._spin_timer.timeout.connect(self._rotate_spinner)
        self._spin_timer.start(80)

        self.set_progress(0, total, '')

    def _rotate_spinner(self):
        self._spin_index = (self._spin_index + 1) % len(self._SPINNER_FRAMES)
        self._spinner_label.setText(self._SPINNER_FRAMES[self._spin_index])

    def set_progress(self, current, total, folder_name):
        self._progress_bar.setMaximum(max(total, 1))
        self._progress_bar.setValue(current)
        if folder_name:
            self._detail_label.setText(f'处理中 ({current}/{total})：{folder_name}')
        else:
            self._detail_label.setText(f'准备处理 {total} 个文件夹...')

    def closeEvent(self, event):
        self._spin_timer.stop()
        super().closeEvent(event)
