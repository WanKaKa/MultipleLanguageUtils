APP_STYLESHEET = """
QWidget#mainWidget {
    background-color: #f3f5f9;
    color: #0f172a;
    font-family: "Segoe UI", "Microsoft YaHei UI", "Microsoft YaHei", sans-serif;
    font-size: 14px;
}

QLabel#brandTitle {
    font-size: 18px;
    font-weight: 700;
    color: #020617;
    padding: 0;
    margin: 0;
}

QLabel#brandSubtitle {
    font-size: 12px;
    color: #475569;
    padding: 0;
    margin: 0;
}

QLabel#fieldLabel {
    background-color: #ffffff;
    color: #334155;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 6px 10px;
    font-size: 13px;
    font-weight: 600;
}

QTextEdit#pathInput {
    background-color: #ffffff;
    color: #000000;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 6px 10px;
    font-size: 16px;
    font-weight: 700;
    selection-background-color: #c7d2fe;
}

QTextEdit#pathInput:hover {
    border-color: #94a3b8;
}

QTextEdit#pathInput:focus {
    border: 1px solid #6366f1;
}

QPushButton {
    border-radius: 8px;
    padding: 6px 6px;
    font-size: 13px;
    font-weight: 600;
    min-height: 30px;
    min-width: 0;
}

QPushButton#primaryButton {
    background-color: qlineargradient(
        x1:0, y1:0, x2:1, y2:1,
        stop:0 #6366f1, stop:1 #818cf8
    );
    color: #ffffff;
    border: none;
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

QPushButton#dangerButton {
    background-color: #f43f5e;
    color: #ffffff;
    border: none;
}

QPushButton#dangerButton:hover {
    background-color: #fb7185;
}

QPushButton#dangerButton:pressed {
    background-color: #e11d48;
}

QMessageBox {
    background-color: #ffffff;
}
"""

ZIP_BUSY_STYLESHEET = """
QDialog#zipBusyDialog {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
}

QLabel#zipSpinner {
    color: #6366f1;
    font-size: 28px;
    font-weight: 700;
}

QLabel#zipBusyTitle {
    color: #0f172a;
    font-size: 16px;
    font-weight: 700;
}

QLabel#zipBusyDetail {
    color: #475569;
    font-size: 13px;
}

QProgressBar#zipBusyProgress {
    background-color: #e2e8f0;
    border: none;
    border-radius: 12px;
    min-height: 24px;
    max-height: 24px;
    text-align: center;
    color: #334155;
    font-size: 15px;
    font-weight: 700;
}

QProgressBar#zipBusyProgress::chunk {
    background-color: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #6366f1, stop:1 #818cf8
    );
    border-radius: 12px;
}
"""


def get_app_stylesheet():
    return APP_STYLESHEET


def get_zip_busy_stylesheet():
    return ZIP_BUSY_STYLESHEET


RESULT_DIALOG_STYLESHEET = """
QDialog#resultDialog {
    background-color: #f3f5f9;
}

QWidget#resultContent {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
}

QLabel#resultText {
    color: #0f172a;
    font-size: 28px;
    font-weight: 700;
    padding: 0 8px;
}
"""


def get_result_dialog_stylesheet():
    return RESULT_DIALOG_STYLESHEET
