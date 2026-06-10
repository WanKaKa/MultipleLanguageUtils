import os
import threading
from io import BytesIO

from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QPixmap, QIntValidator
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QSlider, QSpinBox, QLineEdit, QFileDialog, QTextEdit, QMessageBox, QCheckBox,
    QProgressBar, QSizePolicy, QListWidget, QListWidgetItem,
)

from image_to_webp.styles import get_app_stylesheet
from image_to_webp.utils import DropLineEdit, resolve_path

SUPPORTED_EXTENSIONS = {'.png', '.jpg', '.jpeg'}
DEFAULT_QUALITY = 80
DEFAULT_SMALL_SCALE_PERCENT = 25
SMALL_WEBP_QUALITY_RATIO = 0.75
_Image = None


def _get_image():
    global _Image
    if _Image is None:
        from PIL import Image
        _Image = Image
    return _Image


def collect_image_files(path):
    if os.path.isfile(path):
        ext = os.path.splitext(path)[1].lower()
        return [path] if ext in SUPPORTED_EXTENSIONS else []
    files = []
    for root, _, names in os.walk(path):
        for name in names:
            ext = os.path.splitext(name)[1].lower()
            if ext in SUPPORTED_EXTENSIONS:
                files.append(os.path.join(root, name))
    return sorted(files)


def format_size(size):
    if size < 1024:
        return f'{size} B'
    if size < 1024 * 1024:
        return f'{size / 1024:.1f} KB'
    return f'{size / 1024 / 1024:.2f} MB'


def prepare_image(img):
    if img.mode not in ('RGB', 'RGBA'):
        img = img.convert('RGBA' if 'A' in img.getbands() else 'RGB')
    return img


def encode_webp_bytes(img, quality):
    buffer = BytesIO()
    prepare_image(img).save(buffer, 'WEBP', quality=quality, method=6)
    return buffer.getvalue()


def convert_to_webp(src_path, dst_path, quality, scale_percent=100, target_size=None):
    Image = _get_image()
    with Image.open(src_path) as img:
        img = prepare_image(img)
        if target_size is not None:
            img = img.resize(target_size, Image.Resampling.LANCZOS)
        elif scale_percent < 100:
            width, height = img.size
            new_width = max(1, round(width * scale_percent / 100))
            new_height = max(1, round(height * scale_percent / 100))
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        img.save(dst_path, 'WEBP', quality=quality, method=6)


def small_webp_path(dst_dir, base_name):
    return os.path.join(dst_dir, base_name + '_small.webp')


def small_webp_quality(quality):
    return max(0, min(100, round(quality * SMALL_WEBP_QUALITY_RATIO)))


def calc_small_size(width, height, scale_percent):
    return (
        max(1, round(width * scale_percent / 100)),
        max(1, round(height * scale_percent / 100)),
    )


def calc_small_height(orig_width, orig_height, small_width):
    return max(1, round(small_width * orig_height / orig_width))


def calc_small_width(orig_width, orig_height, small_height):
    return max(1, round(small_height * orig_width / orig_height))


MAX_SMALL_DIMENSION = 99999


def calc_small_size_for_axis(orig_width, orig_height, axis, fixed_width, fixed_height):
    if axis == 'width':
        if fixed_width is None:
            fixed_width, _ = calc_small_size(
                orig_width, orig_height, DEFAULT_SMALL_SCALE_PERCENT
            )
        small_width = fixed_width
        small_height = calc_small_height(orig_width, orig_height, small_width)
    else:
        if fixed_height is None:
            _, fixed_height = calc_small_size(
                orig_width, orig_height, DEFAULT_SMALL_SCALE_PERCENT
            )
        small_height = fixed_height
        small_width = calc_small_width(orig_width, orig_height, small_height)
    return small_width, small_height


def format_resolution_info(width, height, file_size):
    return f'{width}×{height} · {format_size(file_size)}'


class SectionCard(QWidget):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        self.title_label = QLabel(title)
        self.title_label.setObjectName('sectionTitle')
        self.content = QWidget()
        self.content.setObjectName('sectionContent')
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.content_layout.setSpacing(6)

        layout.addWidget(self.title_label)
        layout.addWidget(self.content)

    def body(self):
        return self.content_layout


class PreviewPane(QWidget):
    def __init__(self, badge_text, is_webp=False, parent=None):
        super().__init__(parent)
        self.setObjectName('previewPane')
        self._pixmap = QPixmap()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        header = QHBoxLayout()
        self.badge_label = QLabel(badge_text)
        self.badge_label.setObjectName('previewBadgeWebp' if is_webp else 'previewBadge')
        header.addWidget(self.badge_label)
        header.addStretch()
        layout.addLayout(header)

        self.image_label = QLabel('拖入图片开始预览')
        self.image_label.setObjectName('previewImage')
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label.setMinimumSize(120, 120)
        self.info_label = QLabel('—')
        self.info_label.setObjectName('previewInfo')
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setWordWrap(True)

        layout.addWidget(self.image_label, 1)
        layout.addWidget(self.info_label)

    def set_info(self, text):
        self.info_label.setText(text)

    def set_pixmap(self, pixmap):
        self._pixmap = pixmap
        self._refresh()

    def clear(self, placeholder):
        self._pixmap = QPixmap()
        self.image_label.setPixmap(QPixmap())
        self.image_label.setText(placeholder)
        self.set_info('—')

    def _refresh(self):
        if self._pixmap.isNull():
            return
        self.image_label.setText('')
        size = self.image_label.size()
        if size.width() < 8 or size.height() < 8:
            return
        scaled = self._pixmap.scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(scaled)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._refresh()


class MainWidget(QWidget):
    log_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int, int)
    done_signal = pyqtSignal(bool, str)
    preview_ready_signal = pyqtSignal(QPixmap, QPixmap, str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('mainWidget')
        self._converting = False
        self._previewing = False
        self._image_files = []
        self._image_settings = {}
        self._small_fixed_axis = 'width'
        self._small_fixed_width = None
        self._small_fixed_height = None
        self._loading_quality = False
        self._loading_small_size = False
        self._orig_dimensions = None
        self._preview_timer = QTimer(self)
        self._preview_timer.setSingleShot(True)
        self._preview_timer.setInterval(300)
        self._preview_timer.timeout.connect(self._run_preview)
        self._init_ui()
        self.setStyleSheet(get_app_stylesheet())
        self.log_signal.connect(self._append_log)
        self.progress_signal.connect(self._update_progress)
        self.done_signal.connect(self._on_done)
        self.preview_ready_signal.connect(self._show_preview)
        self.input_path.textChanged.connect(self._on_input_changed)

    def _init_ui(self):
        self.setWindowTitle('PNG/JPG 转 WebP')
        self.resize(1320, 840)
        self.setMinimumSize(1000, 640)

        root = QHBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(14)

        preview_panel = QWidget()
        preview_panel.setObjectName('previewArea')
        preview_layout = QVBoxLayout(preview_panel)
        preview_layout.setContentsMargins(12, 12, 12, 12)
        preview_layout.setSpacing(10)

        preview_header = QHBoxLayout()
        preview_header.setSpacing(10)
        preview_title = QLabel('预览工作台')
        preview_title.setObjectName('brandTitle')
        self.current_file_label = QLabel('尚未选择文件')
        self.current_file_label.setObjectName('currentFileLabel')
        self.current_file_label.setWordWrap(True)
        preview_header.addWidget(preview_title, 0, Qt.AlignVCenter)
        preview_header.addWidget(self.current_file_label, 1, Qt.AlignVCenter)
        preview_layout.addLayout(preview_header)

        preview_row = QHBoxLayout()
        preview_row.setSpacing(10)
        self.orig_pane = PreviewPane('ORIGINAL')
        self.webp_pane = PreviewPane('WEBP', is_webp=True)
        preview_row.addWidget(self.orig_pane, 1)
        preview_row.addWidget(self.webp_pane, 1)
        preview_layout.addLayout(preview_row, 1)

        root.addWidget(preview_panel, 1)

        control_panel = QWidget()
        control_panel.setObjectName('sidebar')
        control_panel.setFixedWidth(380)
        control_layout = QVBoxLayout(control_panel)
        control_layout.setContentsMargins(12, 12, 12, 12)
        control_layout.setSpacing(10)

        title = QLabel('WebP Studio')
        title.setObjectName('brandTitle')
        subtitle = QLabel('逐张调参 · 实时预览 · 批量导出')
        subtitle.setObjectName('brandSubtitle')
        control_layout.addWidget(title)
        control_layout.addWidget(subtitle)

        input_section = SectionCard('输入源')
        input_layout = input_section.body()
        self.input_path = DropLineEdit()
        self.input_path.setPlaceholderText('拖入文件、文件夹或快捷方式')
        btn_row = QHBoxLayout()
        btn_file = QPushButton('选择文件')
        btn_file.setObjectName('ghostButton')
        btn_file.clicked.connect(self._select_file)
        btn_dir = QPushButton('选择文件夹')
        btn_dir.setObjectName('ghostButton')
        btn_dir.clicked.connect(self._select_dir)
        btn_row.addWidget(btn_file)
        btn_row.addWidget(btn_dir)
        input_layout.addWidget(self.input_path)
        input_layout.addLayout(btn_row)
        control_layout.addWidget(input_section)

        list_section = SectionCard('图片队列')
        list_layout = list_section.body()
        list_header = QHBoxLayout()
        self.setup_status_label = QLabel('0 张')
        self.setup_status_label.setObjectName('statusBadge')
        list_header.addStretch()
        list_header.addWidget(self.setup_status_label)
        list_layout.addLayout(list_header)
        self.image_list = QListWidget()
        self.image_list.currentRowChanged.connect(self._on_image_selected)
        list_layout.addWidget(self.image_list)
        nav_row = QHBoxLayout()
        self.prev_btn = QPushButton('‹ 上一张')
        self.prev_btn.setObjectName('ghostButton')
        self.prev_btn.clicked.connect(self._select_prev_image)
        self.next_btn = QPushButton('下一张 ›')
        self.next_btn.setObjectName('ghostButton')
        self.next_btn.clicked.connect(self._select_next_image)
        nav_row.addWidget(self.prev_btn)
        nav_row.addWidget(self.next_btn)
        list_layout.addLayout(nav_row)
        control_layout.addWidget(list_section, 1)

        quality_section = SectionCard('清晰度')
        quality_layout = quality_section.body()
        quality_top = QHBoxLayout()
        self.quality_value_label = QLabel(str(DEFAULT_QUALITY))
        self.quality_value_label.setObjectName('qualityValue')
        self.quality_value_label.setAlignment(Qt.AlignCenter)
        quality_meta = QVBoxLayout()
        quality_meta.setSpacing(0)
        quality_meta.addWidget(self.quality_value_label)
        unit = QLabel('/ 100')
        unit.setObjectName('qualityUnit')
        unit.setAlignment(Qt.AlignCenter)
        quality_meta.addWidget(unit)
        quality_top.addLayout(quality_meta)
        slider_col = QVBoxLayout()
        hint = QLabel('数值越高，画质越好，文件越大')
        hint.setObjectName('hintLabel')
        slider_row = QHBoxLayout()
        self.quality_slider = QSlider(Qt.Horizontal)
        self.quality_slider.setRange(0, 100)
        self.quality_slider.setValue(DEFAULT_QUALITY)
        self.quality_spin = QSpinBox()
        self.quality_spin.setRange(0, 100)
        self.quality_spin.setValue(DEFAULT_QUALITY)
        self.quality_spin.setFixedWidth(68)
        self.quality_slider.valueChanged.connect(self.quality_spin.setValue)
        self.quality_spin.valueChanged.connect(self.quality_slider.setValue)
        self.quality_slider.valueChanged.connect(self._on_quality_changed)
        self.quality_spin.valueChanged.connect(self._on_quality_changed)
        slider_row.addWidget(self.quality_slider)
        slider_row.addWidget(self.quality_spin)
        slider_col.addWidget(hint)
        slider_col.addLayout(slider_row)
        quality_top.addLayout(slider_col, 1)
        quality_layout.addLayout(quality_top)
        control_layout.addWidget(quality_section)

        output_section = SectionCard('输出设置')
        output_layout = output_section.body()
        self.same_dir_check = QCheckBox('保存到原文件同目录')
        self.same_dir_check.setChecked(True)
        self.same_dir_check.toggled.connect(self._toggle_output_dir)
        output_layout.addWidget(self.same_dir_check)
        out_row = QHBoxLayout()
        self.output_path = DropLineEdit(
            prefer_dir=True,
            before_drop=self._enable_custom_output,
        )
        self.output_path.setPlaceholderText('拖入自定义输出目录')
        self.output_path.setReadOnly(True)
        btn_out_dir = QPushButton('浏览')
        btn_out_dir.setObjectName('ghostButton')
        btn_out_dir.setFixedWidth(64)
        btn_out_dir.clicked.connect(self._select_output_dir)
        self.btn_out_dir = btn_out_dir
        out_row.addWidget(self.output_path)
        out_row.addWidget(btn_out_dir)
        output_layout.addLayout(out_row)
        self.delete_original_check = QCheckBox('转换成功后删除原图')
        self.delete_original_check.setChecked(True)
        output_layout.addWidget(self.delete_original_check)
        self.generate_small_check = QCheckBox('同时生成小尺寸 WebP')
        self.generate_small_check.setChecked(True)
        output_layout.addWidget(self.generate_small_check)
        small_row = QHBoxLayout()
        small_row.addWidget(QLabel('小图尺寸'))
        self.small_width_input = QLineEdit()
        self.small_width_input.setAlignment(Qt.AlignCenter)
        self.small_width_input.setEnabled(False)
        self.small_width_input.setFixedWidth(72)
        self.small_width_input.setPlaceholderText('—')
        small_row.addWidget(self.small_width_input)
        small_row.addWidget(QLabel('×'))
        self.small_height_input = QLineEdit()
        self.small_height_input.setAlignment(Qt.AlignCenter)
        self.small_height_input.setEnabled(False)
        self.small_height_input.setFixedWidth(72)
        self.small_height_input.setPlaceholderText('—')
        small_row.addWidget(self.small_height_input)
        small_row.addStretch()
        output_layout.addLayout(small_row)
        self.generate_small_check.toggled.connect(self._update_small_controls_enabled)
        self.generate_small_check.toggled.connect(self._refresh_resolution_info)
        self.small_width_input.editingFinished.connect(self._on_small_width_edited)
        self.small_height_input.editingFinished.connect(self._on_small_height_edited)
        control_layout.addWidget(output_section)

        action_section = SectionCard('导出')
        action_layout = action_section.body()
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.convert_btn = QPushButton('全部生成 WebP')
        self.convert_btn.setObjectName('primaryButton')
        self.convert_btn.setMinimumHeight(36)
        self.convert_btn.setEnabled(False)
        self.convert_btn.clicked.connect(self._start_convert)
        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setMaximumHeight(80)
        self.log_view.setPlaceholderText('等待开始转换...')
        action_layout.addWidget(self.progress_bar)
        action_layout.addWidget(self.convert_btn)
        action_layout.addWidget(self.log_view)
        control_layout.addWidget(action_section)

        root.addWidget(control_panel)

    def _toggle_output_dir(self, checked):
        self.output_path.setReadOnly(checked)
        self.btn_out_dir.setEnabled(not checked)

    def _enable_custom_output(self):
        if self.same_dir_check.isChecked():
            self.same_dir_check.setChecked(False)

    def _select_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, '选择图片', '',
            '图片文件 (*.png *.jpg *.jpeg);;所有文件 (*.*)'
        )
        if path:
            self.input_path.setText(path)

    def _select_dir(self):
        path = QFileDialog.getExistingDirectory(self, '选择文件夹')
        if path:
            self.input_path.setText(path)

    def _select_output_dir(self):
        path = QFileDialog.getExistingDirectory(self, '选择输出目录')
        if path:
            self.output_path.setText(path)

    def _get_resolved_input_path(self):
        raw = self.input_path.text().strip()
        path = resolve_path(raw)
        if path and path != raw:
            self.input_path.blockSignals(True)
            self.input_path.setText(path)
            self.input_path.blockSignals(False)
        return path

    def _on_input_changed(self):
        path = self._get_resolved_input_path()
        files = collect_image_files(path) if path and os.path.exists(path) else []
        self._image_files = files
        self._image_settings = {file_path: DEFAULT_QUALITY for file_path in files}

        self.image_list.blockSignals(True)
        self.image_list.clear()
        for file_path in files:
            item = QListWidgetItem(self._format_list_text(file_path))
            item.setData(Qt.UserRole, file_path)
            self.image_list.addItem(item)
        self.image_list.blockSignals(False)

        self._update_setup_status()
        self._update_convert_btn()

        if files:
            self.image_list.setCurrentRow(0)
            self._on_image_selected(0)
        else:
            self.current_file_label.setText('尚未选择文件')
            self._clear_preview('拖入图片开始预览')

    def _format_list_text(self, file_path):
        name = os.path.basename(file_path)
        return f'{name}  ·  Q{self._image_settings[file_path]}'

    def _update_list_item(self, file_path):
        row = self._image_files.index(file_path)
        item = self.image_list.item(row)
        item.setText(self._format_list_text(file_path))

    def _current_path(self):
        row = self.image_list.currentRow()
        if row < 0 or row >= len(self._image_files):
            return None
        return self._image_files[row]

    def _set_quality_display(self, quality):
        self.quality_value_label.setText(str(quality))

    def _apply_quality_to_controls(self, quality):
        self._loading_quality = True
        self.quality_slider.blockSignals(True)
        self.quality_spin.blockSignals(True)
        self.quality_slider.setValue(quality)
        self.quality_spin.setValue(quality)
        self.quality_slider.blockSignals(False)
        self.quality_spin.blockSignals(False)
        self._set_quality_display(quality)
        self._loading_quality = False

    def _on_image_selected(self, row):
        if row < 0 or row >= len(self._image_files):
            return
        file_path = self._image_files[row]
        self.current_file_label.setText(file_path)
        self._apply_quality_to_controls(self._image_settings[file_path])
        self._refresh_resolution_info()
        self._schedule_preview()

    def _on_quality_changed(self, value):
        if self._loading_quality:
            return
        self._set_quality_display(value)
        file_path = self._current_path()
        if not file_path:
            return
        self._image_settings[file_path] = value
        self._update_list_item(file_path)
        self._schedule_preview()

    def _select_prev_image(self):
        row = self.image_list.currentRow()
        if row > 0:
            self.image_list.setCurrentRow(row - 1)

    def _select_next_image(self):
        row = self.image_list.currentRow()
        if row < self.image_list.count() - 1:
            self.image_list.setCurrentRow(row + 1)

    def _update_setup_status(self):
        count = len(self._image_files)
        self.setup_status_label.setText(f'{count} 张')

    def _update_convert_btn(self):
        self.convert_btn.setEnabled(len(self._image_files) > 0 and not self._converting)

    def _schedule_preview(self):
        if self._converting:
            return
        self._preview_timer.start()

    def _run_preview(self):
        preview_path = self._current_path()
        if not preview_path or not os.path.isfile(preview_path):
            self._clear_preview('拖入图片开始预览')
            return
        if self._previewing:
            self._schedule_preview()
            return

        quality = self.quality_spin.value()
        self._previewing = True
        self.webp_pane.clear('正在生成预览...')
        thread = threading.Thread(
            target=self._preview_task,
            args=(preview_path, quality),
            daemon=True,
        )
        thread.start()

    def _preview_task(self, src_path, quality):
        try:
            Image = _get_image()
            orig_size = os.path.getsize(src_path)
            orig_pixmap = QPixmap(src_path)
            with Image.open(src_path) as img:
                width, height = img.size
                webp_bytes = encode_webp_bytes(img, quality)
            webp_pixmap = QPixmap()
            webp_pixmap.loadFromData(webp_bytes, 'WEBP')
            webp_size = len(webp_bytes)
            saved = orig_size - webp_size
            saved_pct = (saved / orig_size * 100) if orig_size else 0
            orig_info = format_resolution_info(width, height, orig_size)
            webp_info = f'{format_size(webp_size)}  ·  Q{quality}'
            if saved > 0:
                webp_info += f'  ·  -{format_size(saved)} ({saved_pct:.1f}%)'
            else:
                webp_info += f'  ·  +{format_size(-saved)} ({-saved_pct:.1f}%)'
            self.preview_ready_signal.emit(orig_pixmap, webp_pixmap, orig_info, webp_info)
        except Exception as e:
            self.preview_ready_signal.emit(QPixmap(), QPixmap(), '—', f'预览失败: {e}')
        finally:
            self._previewing = False

    def _show_preview(self, orig_pixmap, webp_pixmap, orig_info, webp_info):
        if orig_pixmap.isNull():
            self._clear_preview('预览失败')
            self.webp_pane.set_info(webp_info)
            return
        self.orig_pane.set_pixmap(orig_pixmap)
        self.orig_pane.set_info(orig_info)
        if webp_pixmap.isNull():
            self.webp_pane.clear('WebP 预览失败')
            return
        self.webp_pane.set_pixmap(webp_pixmap)
        self.webp_pane.set_info(webp_info)

    def _update_small_controls_enabled(self):
        enabled = (
            self.generate_small_check.isChecked()
            and self._orig_dimensions is not None
        )
        self.small_width_input.setEnabled(enabled)
        self.small_height_input.setEnabled(enabled)

    def _set_small_dimensions(self, small_width, small_height):
        self._loading_small_size = True
        self.small_width_input.setText(str(small_width))
        self.small_height_input.setText(str(small_height))
        self._loading_small_size = False

    def _clear_small_dimensions(self):
        self._loading_small_size = True
        self.small_width_input.clear()
        self.small_height_input.clear()
        self._loading_small_size = False

    def _update_small_dimension_validators(self):
        validator = QIntValidator(1, MAX_SMALL_DIMENSION, self)
        self.small_width_input.setValidator(validator)
        self.small_height_input.setValidator(validator)

    def _parse_small_dimension(self, text):
        text = text.strip()
        if not text:
            return None
        try:
            value = int(text)
        except ValueError:
            return None
        return max(1, min(MAX_SMALL_DIMENSION, value))

    def _ensure_small_fixed_defaults(self, orig_width, orig_height):
        if self._small_fixed_width is None and self._small_fixed_height is None:
            default_width, _ = calc_small_size(
                orig_width, orig_height, DEFAULT_SMALL_SCALE_PERCENT
            )
            self._small_fixed_axis = 'width'
            self._small_fixed_width = default_width

    def _sync_small_dimensions_display(self):
        if not self._orig_dimensions:
            return
        orig_width, orig_height = self._orig_dimensions
        self._ensure_small_fixed_defaults(orig_width, orig_height)
        small_width, small_height = calc_small_size_for_axis(
            orig_width,
            orig_height,
            self._small_fixed_axis,
            self._small_fixed_width,
            self._small_fixed_height,
        )
        self._set_small_dimensions(small_width, small_height)

    def _apply_small_width(self, small_width):
        self._small_fixed_axis = 'width'
        self._small_fixed_width = small_width
        if not self._orig_dimensions:
            return
        orig_width, orig_height = self._orig_dimensions
        small_height = calc_small_height(orig_width, orig_height, small_width)
        self._loading_small_size = True
        self.small_height_input.setText(str(small_height))
        self._loading_small_size = False

    def _apply_small_height(self, small_height):
        self._small_fixed_axis = 'height'
        self._small_fixed_height = small_height
        if not self._orig_dimensions:
            return
        orig_width, orig_height = self._orig_dimensions
        small_width = calc_small_width(orig_width, orig_height, small_height)
        self._loading_small_size = True
        self.small_width_input.setText(str(small_width))
        self._loading_small_size = False

    def _normalize_small_dimension_input(self, line_edit, parsed_value):
        try:
            entered = int(line_edit.text().strip())
        except ValueError:
            entered = None
        if entered != parsed_value:
            self._loading_small_size = True
            line_edit.setText(str(parsed_value))
            self._loading_small_size = False

    def _on_small_width_edited(self):
        if self._loading_small_size or not self._orig_dimensions:
            return
        small_width = self._parse_small_dimension(self.small_width_input.text())
        if small_width is None:
            self._sync_small_dimensions_display()
            return
        self._normalize_small_dimension_input(self.small_width_input, small_width)
        self._apply_small_width(small_width)

    def _on_small_height_edited(self):
        if self._loading_small_size or not self._orig_dimensions:
            return
        small_height = self._parse_small_dimension(self.small_height_input.text())
        if small_height is None:
            self._sync_small_dimensions_display()
            return
        self._normalize_small_dimension_input(self.small_height_input, small_height)
        self._apply_small_height(small_height)

    def _refresh_resolution_info(self):
        preview_path = self._current_path()
        if not preview_path or not os.path.isfile(preview_path):
            self._orig_dimensions = None
            self._clear_small_dimensions()
            self._update_small_controls_enabled()
            return
        try:
            Image = _get_image()
            with Image.open(preview_path) as img:
                width, height = img.size
            self._orig_dimensions = (width, height)
            self._update_small_dimension_validators()
            orig_size = os.path.getsize(preview_path)
            self.orig_pane.set_info(format_resolution_info(width, height, orig_size))
            self._sync_small_dimensions_display()
            self._update_small_controls_enabled()
        except Exception:
            self._orig_dimensions = None
            self._update_small_controls_enabled()

    def _clear_preview(self, placeholder):
        self.orig_pane.clear(placeholder)
        self.webp_pane.clear('调整滑块查看效果')
        self._orig_dimensions = None
        self._clear_small_dimensions()
        self._update_small_controls_enabled()

    def _append_log(self, text):
        self.log_view.append(text)

    def _update_progress(self, current, total):
        if total <= 0:
            self.progress_bar.setValue(0)
            return
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(current)

    def _on_done(self, success, message):
        self._converting = False
        if self.delete_original_check.isChecked():
            self._on_input_changed()
        self._update_convert_btn()
        self._schedule_preview()
        if success:
            QMessageBox.information(self, '完成', message)
        else:
            QMessageBox.warning(self, '提示', message)

    def _start_convert(self):
        if self._converting:
            return

        if not self._image_files:
            QMessageBox.warning(self, '提示', '请先选择图片')
            return

        use_same_dir = self.same_dir_check.isChecked()
        output_dir = resolve_path(self.output_path.text().strip())
        if output_dir != self.output_path.text().strip():
            self.output_path.setText(output_dir)
        if not use_same_dir:
            if not output_dir:
                QMessageBox.warning(self, '提示', '请选择输出目录，或勾选输出到原文件同目录')
                return
            if not os.path.isdir(output_dir):
                QMessageBox.warning(self, '提示', '输出目录不存在')
                return

        self._converting = True
        self.convert_btn.setEnabled(False)
        self.log_view.clear()
        self.progress_bar.setValue(0)
        self.log_signal.emit(f'开始生成 {len(self._image_files)} 个 WebP 文件')

        delete_original = self.delete_original_check.isChecked()
        generate_small = self.generate_small_check.isChecked()
        thread = threading.Thread(
            target=self._convert_task,
            args=(use_same_dir, output_dir, delete_original, generate_small),
            daemon=True,
        )
        thread.start()

    def _convert_task(self, use_same_dir, output_dir, delete_original, generate_small):
        success_count = 0
        small_success_count = 0
        fail_count = 0
        skip_count = 0
        small_skip_count = 0
        delete_count = 0
        delete_fail_count = 0
        total = len(self._image_files)
        converted_any = False

        for i, src_path in enumerate(self._image_files, start=1):
            quality = self._image_settings[src_path]
            try:
                if use_same_dir:
                    dst_dir = os.path.dirname(src_path)
                else:
                    dst_dir = output_dir

                base_name = os.path.splitext(os.path.basename(src_path))[0]
                dst_path = os.path.join(dst_dir, base_name + '.webp')
                file_converted = False

                if os.path.exists(dst_path):
                    skip_count += 1
                    self.log_signal.emit(f'[跳过] {dst_path} 已存在')
                else:
                    convert_to_webp(src_path, dst_path, quality)
                    self.log_signal.emit(f'[成功] {src_path} -> {dst_path} (Q:{quality})')
                    success_count += 1
                    file_converted = True
                    converted_any = True

                if generate_small:
                    small_dst_path = small_webp_path(dst_dir, base_name)
                    if os.path.exists(small_dst_path):
                        small_skip_count += 1
                        self.log_signal.emit(f'[跳过] {small_dst_path} 已存在')
                    else:
                        Image = _get_image()
                        with Image.open(src_path) as img:
                            orig_width, orig_height = img.size
                        small_width, small_height = calc_small_size_for_axis(
                            orig_width,
                            orig_height,
                            self._small_fixed_axis,
                            self._small_fixed_width,
                            self._small_fixed_height,
                        )
                        small_quality = small_webp_quality(quality)
                        convert_to_webp(
                            src_path,
                            small_dst_path,
                            small_quality,
                            target_size=(small_width, small_height),
                        )
                        self.log_signal.emit(
                            f'[成功] {src_path} -> {small_dst_path} '
                            f'(Q:{small_quality}, {small_width}×{small_height})'
                        )
                        small_success_count += 1
                        file_converted = True
                        converted_any = True

                if file_converted and delete_original:
                    try:
                        os.remove(src_path)
                        delete_count += 1
                        self.log_signal.emit(f'[删除] {src_path}')
                    except Exception as e:
                        delete_fail_count += 1
                        self.log_signal.emit(f'[删除失败] {src_path}: {e}')
            except Exception as e:
                fail_count += 1
                self.log_signal.emit(f'[失败] {src_path}: {e}')

            self.progress_signal.emit(i, total)

        message = (
            f'转换完成：成功 {success_count} 个，失败 {fail_count} 个，跳过 {skip_count} 个'
        )
        if generate_small:
            message += f'；小图成功 {small_success_count} 个，跳过 {small_skip_count} 个'
        if delete_original and converted_any:
            message += f'，已删除原图 {delete_count} 个'
            if delete_fail_count:
                message += f'，删除失败 {delete_fail_count} 个'
        self.log_signal.emit(message)
        self.done_signal.emit(fail_count == 0 and delete_fail_count == 0, message)
