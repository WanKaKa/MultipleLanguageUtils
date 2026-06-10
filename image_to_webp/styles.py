import os
import sys


def _assets_dir():
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, 'assets')
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')


def _asset_url(filename):
    return os.path.join(_assets_dir(), filename).replace('\\', '/')


def get_app_stylesheet():
    return (
        APP_STYLESHEET
        .replace('{slider_handle}', _asset_url('slider_handle.png'))
        .replace('{slider_handle_hover}', _asset_url('slider_handle_hover.png'))
        .replace('{checkbox_unchecked}', _asset_url('checkbox_unchecked.png'))
        .replace('{checkbox_checked}', _asset_url('checkbox_checked.png'))
    )


APP_STYLESHEET = """
QWidget#mainWidget {
    background-color: #f3f5f9;
    color: #0f172a;
    font-family: "Segoe UI", "Microsoft YaHei UI", "Microsoft YaHei", sans-serif;
    font-size: 15px;
}

QWidget#previewArea {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
}

QWidget#sidebar {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
}

QLabel#brandTitle {
    font-size: 24px;
    font-weight: 700;
    color: #020617;
    letter-spacing: 0.3px;
}

QLabel#brandSubtitle {
    font-size: 14px;
    color: #475569;
    padding-bottom: 4px;
}

QLabel#sectionTitle {
    font-size: 13px;
    font-weight: 700;
    color: #64748b;
    letter-spacing: 1px;
    padding-left: 2px;
}

QWidget#sectionContent {
    background-color: #f8fafc;
    border: 1px solid #e8edf3;
    border-radius: 12px;
}

QLabel#currentFileLabel {
    background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 7px 10px;
    color: #1e293b;
    font-size: 14px;
}

QLabel#statusBadge {
    background-color: #eef2ff;
    color: #3730a3;
    border: 1px solid #c7d2fe;
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 14px;
    font-weight: 600;
}

QLabel#hintLabel {
    color: #475569;
    font-size: 13px;
}

QLabel#qualityValue {
    font-size: 32px;
    font-weight: 700;
    color: #4338ca;
    min-width: 52px;
}

QLabel#qualityUnit {
    font-size: 13px;
    color: #475569;
    padding-top: 10px;
}

QLineEdit {
    background-color: #ffffff;
    color: #0f172a;
    border: 1px solid #cbd5e1;
    border-radius: 10px;
    padding: 10px 12px;
    font-size: 14px;
    selection-background-color: #c7d2fe;
}

QLineEdit:hover {
    border-color: #94a3b8;
}

QLineEdit:focus {
    border: 1px solid #6366f1;
    background-color: #ffffff;
}

QLineEdit:read-only {
    color: #334155;
    background-color: #f1f5f9;
}

QPushButton {
    background-color: #ffffff;
    color: #1e293b;
    border: 1px solid #cbd5e1;
    border-radius: 10px;
    padding: 10px 14px;
    font-size: 14px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #f8fafc;
    border-color: #94a3b8;
    color: #020617;
}

QPushButton:pressed {
    background-color: #f1f5f9;
}

QPushButton:disabled {
    background-color: #f8fafc;
    color: #94a3b8;
    border-color: #e2e8f0;
}

QPushButton#ghostButton {
    background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    color: #334155;
    font-size: 14px;
}

QPushButton#ghostButton:hover {
    background-color: #eef2ff;
    border-color: #c7d2fe;
    color: #312e81;
}

QPushButton#primaryButton {
    background-color: qlineargradient(
        x1:0, y1:0, x2:1, y2:1,
        stop:0 #6366f1, stop:1 #818cf8
    );
    color: #ffffff;
    border: none;
    font-size: 16px;
    font-weight: 700;
    padding: 12px 18px;
    border-radius: 12px;
}

QPushButton#primaryButton:hover {
    background-color: qlineargradient(
        x1:0, y1:0, x2:1, y2:1,
        stop:0 #7577f5, stop:1 #9399fb
    );
}

QPushButton#primaryButton:pressed {
    background-color: #4f46e5;
}

QPushButton#primaryButton:disabled {
    background-color: #e2e8f0;
    color: #94a3b8;
}

QListWidget {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 6px;
    outline: none;
    color: #1e293b;
    font-size: 14px;
}

QListWidget::item {
    border-radius: 8px;
    padding: 11px 12px;
    margin: 2px 0;
}

QListWidget::item:selected {
    background-color: #eef2ff;
    color: #312e81;
    border: 1px solid #c7d2fe;
    font-weight: 600;
}

QListWidget::item:hover {
    background-color: #f8fafc;
    color: #0f172a;
}

QSlider::groove:horizontal {
    height: 5px;
    background: #e2e8f0;
    border-radius: 2px;
}

QSlider::handle:horizontal {
    image: url({slider_handle});
    width: 22px;
    height: 22px;
    margin: -9px 0;
    background: transparent;
    border: none;
}

QSlider::handle:horizontal:hover {
    image: url({slider_handle_hover});
}

QSlider::sub-page:horizontal {
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #6366f1, stop:1 #38bdf8
    );
    border-radius: 2px;
}

QSpinBox {
    background-color: #ffffff;
    color: #312e81;
    border: 1px solid #cbd5e1;
    border-radius: 10px;
    padding: 8px;
    font-size: 15px;
    font-weight: 700;
}

QSpinBox:focus {
    border-color: #6366f1;
}

QCheckBox {
    spacing: 10px;
    color: #1e293b;
    font-size: 14px;
}

QCheckBox::indicator {
    width: 20px;
    height: 20px;
    image: url({checkbox_unchecked});
    border: none;
    background: transparent;
}

QCheckBox::indicator:checked {
    image: url({checkbox_checked});
    border: none;
    background: transparent;
}

QProgressBar {
    background-color: #e2e8f0;
    border: none;
    border-radius: 8px;
    height: 8px;
    text-align: center;
    color: #475569;
    font-size: 12px;
}

QProgressBar::chunk {
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #6366f1, stop:1 #38bdf8
    );
    border-radius: 8px;
}

QTextEdit {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 10px;
    color: #334155;
    font-family: "Cascadia Mono", "Consolas", "Microsoft YaHei", monospace;
    font-size: 13px;
}

QWidget#previewPane {
    background-color: #f8fafc;
    border: 1px solid #e8edf3;
    border-radius: 14px;
}

QLabel#previewBadge {
    background-color: #f1f5f9;
    color: #475569;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 3px 10px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
}

QLabel#previewBadgeWebp {
    background-color: #eef2ff;
    color: #3730a3;
    border: 1px solid #c7d2fe;
    border-radius: 12px;
    padding: 3px 10px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
}

QLabel#previewImage {
    background-color: #e9edf3;
    border: 1px solid #d8dee8;
    border-radius: 10px;
    color: #64748b;
    font-size: 14px;
}

QLabel#previewInfo {
    color: #000000;
    font-size: 14px;
    font-weight: bold;
    padding: 0;
}

QScrollBar:vertical {
    background: #f1f5f9;
    width: 8px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background: #cbd5e1;
    border-radius: 4px;
    min-height: 24px;
}

QScrollBar::handle:vertical:hover {
    background: #6366f1;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}
"""
