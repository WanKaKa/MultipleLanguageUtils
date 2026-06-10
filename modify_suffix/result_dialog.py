import math
import re

from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QColor, QPainter, QPen
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QWidget

from modify_suffix.styles import get_result_dialog_stylesheet

_ZIP_RESULT_RE = re.compile(
    r'^(压缩|解压)完成：成功 (\d+) 个，跳过 (\d+) 个，失败 (\d+) 个',
)


def _display_text(message, success):
    match = _ZIP_RESULT_RE.match(message.strip())
    if match:
        action = match.group(1)
        fail_count = int(match.group(4))
        if success and fail_count == 0:
            return f'{action}成功'
        return f'{action}失败'

    if message == '成功':
        return '成功'

    return message.split('\n')[0]


def _ease_out_cubic(value):
    return 1 - (1 - value) ** 3


class ResultAnimWidget(QWidget):
    ANIM_DURATION_MS = 900
    FRAME_MS = 16

    def __init__(self, success=True, parent=None):
        super().__init__(parent)
        self._success = success
        self._elapsed = 0
        self.setFixedSize(108, 108)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(self.FRAME_MS)

    def _tick(self):
        self._elapsed += self.FRAME_MS
        self.update()
        if self._elapsed >= self.ANIM_DURATION_MS:
            self._timer.stop()

    def stop(self):
        self._timer.stop()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        progress = min(1.0, self._elapsed / self.ANIM_DURATION_MS)
        center_x = self.width() / 2
        center_y = self.height() / 2
        radius = 36

        if self._success:
            self._paint_success(painter, center_x, center_y, radius, progress)
        else:
            self._paint_failure(painter, center_x, center_y, radius, progress)

    def _paint_circle(self, painter, center_x, center_y, radius, progress, halo_color, fill_color):
        scale = _ease_out_cubic(min(1.0, progress / 0.42))
        if scale <= 0:
            return

        current_radius = radius * scale
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(halo_color))
        painter.drawEllipse(QPointF(center_x, center_y), current_radius, current_radius)

        inner_radius = current_radius * 0.9
        painter.setBrush(QColor(fill_color))
        painter.drawEllipse(QPointF(center_x, center_y), inner_radius, inner_radius)

    def _paint_success(self, painter, center_x, center_y, radius, progress):
        self._paint_circle(
            painter, center_x, center_y, radius, progress,
            '#dcfce7', '#22c55e',
        )

        mark_progress = max(0.0, min(1.0, (progress - 0.32) / 0.45))
        if mark_progress <= 0:
            return

        pen = QPen(QColor('#ffffff'))
        pen.setWidth(6)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        painter.setPen(pen)

        start = QPointF(center_x - 16, center_y + 1)
        middle = QPointF(center_x - 3, center_y + 14)
        end = QPointF(center_x + 20, center_y - 12)

        first_len = math.hypot(middle.x() - start.x(), middle.y() - start.y())
        second_len = math.hypot(end.x() - middle.x(), end.y() - middle.y())
        total_len = first_len + second_len
        draw_len = total_len * _ease_out_cubic(mark_progress)

        if draw_len <= first_len:
            ratio = draw_len / first_len if first_len else 1
            painter.drawLine(
                start,
                QPointF(
                    start.x() + (middle.x() - start.x()) * ratio,
                    start.y() + (middle.y() - start.y()) * ratio,
                ),
            )
            return

        painter.drawLine(start, middle)
        remain = draw_len - first_len
        ratio = remain / second_len if second_len else 1
        painter.drawLine(
            middle,
            QPointF(
                middle.x() + (end.x() - middle.x()) * ratio,
                middle.y() + (end.y() - middle.y()) * ratio,
            ),
        )

    def _paint_failure(self, painter, center_x, center_y, radius, progress):
        self._paint_circle(
            painter, center_x, center_y, radius, progress,
            '#fee2e2', '#ef4444',
        )

        mark_progress = max(0.0, min(1.0, (progress - 0.32) / 0.45))
        if mark_progress <= 0:
            return

        pen = QPen(QColor('#ffffff'))
        pen.setWidth(6)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)

        offset = 13 * _ease_out_cubic(mark_progress)
        painter.drawLine(
            QPointF(center_x - offset, center_y - offset),
            QPointF(center_x + offset, center_y + offset),
        )
        painter.drawLine(
            QPointF(center_x + offset, center_y - offset),
            QPointF(center_x - offset, center_y + offset),
        )


class ResultDialog(QDialog):
    def __init__(self, parent, message, success=True, title=''):
        super().__init__(parent)
        self.setObjectName('resultDialog')
        self.setWindowTitle(title)
        self.setWindowModality(Qt.WindowModal)
        self.setMinimumWidth(360)
        self.setStyleSheet(get_result_dialog_stylesheet())

        root = QVBoxLayout(self)
        root.setContentsMargins(7, 7, 7, 7)

        content = QWidget(self)
        content.setObjectName('resultContent')

        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(15, 13, 15, 24)
        content_layout.setSpacing(8)
        content_layout.setAlignment(Qt.AlignCenter)

        self._anim_widget = ResultAnimWidget(success=success, parent=content)
        content_layout.addWidget(self._anim_widget, 0, Qt.AlignCenter)

        text_label = QLabel(_display_text(message, success))
        text_label.setObjectName('resultText')
        text_label.setWordWrap(True)
        text_label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(text_label)

        root.addWidget(content)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter, Qt.Key_Escape):
            self.accept()
            return
        super().keyPressEvent(event)

    def mousePressEvent(self, event):
        self.accept()

    def closeEvent(self, event):
        self._anim_widget.stop()
        super().closeEvent(event)


def show_result(parent, title, message, kind='info'):
    success = kind == 'success'
    dialog = ResultDialog(parent, message, success=success, title=title)
    dialog.exec_()


def show_zip_result(parent, success, message, title=''):
    dialog = ResultDialog(parent, message, success=success, title=title)
    dialog.exec_()
