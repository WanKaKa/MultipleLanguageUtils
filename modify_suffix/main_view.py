import os
import shutil
import threading

from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtWidgets import QWidget, QSizePolicy
from PyQt5 import QtGui

from modify_suffix import main_ui, utils, path_ex, database
from modify_suffix.file_type import extensions_are_equivalent, guess_file_extension
from modify_suffix.result_dialog import show_result, show_zip_result
from modify_suffix.styles import get_app_stylesheet
from modify_suffix.zip_busy_dialog import ZipBusyDialog


class MainWindow(QWidget, main_ui.Ui_Form):
    zip_progress_signal = pyqtSignal(int, int, str)
    zip_done_signal = pyqtSignal(bool, str)

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self._zip_running = False
        self._zip_progress_dialog = None
        self.zip_progress_signal.connect(self._on_zip_progress)
        self.zip_done_signal.connect(self._on_zip_done)
        self._apply_theme()

        self.setWindowTitle('文件后缀工具')
        filename = utils.resource_path(os.path.join('image', 'fast.ico'))
        if os.path.exists(filename):
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(filename))
            self.setWindowIcon(icon)

        self.init_view()
        self.init_ui()

        self.input_001_value = None
        self.input_002_value = None
        self.input_003_value = None
        self.input_004_value = None
        self.input_005_value = None

        self.old_suffix = None
        self.new_suffix = None
        self.work_path = None

    def _apply_theme(self):
        self.setObjectName('mainWidget')
        self.setStyleSheet(get_app_stylesheet())
        self.FIELD_LABEL_WIDTH = 180
        self.formLayout.setContentsMargins(12, 8, 12, 12)
        self.formLayout.setHorizontalSpacing(0)
        self.formLayout.setVerticalSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(12)

        for label in (
            self.label_4, self.label_5, self.label, self.label_2, self.label_3
        ):
            label.setObjectName('fieldLabel')
            label.setStyleSheet('')
            label.setFixedWidth(self.FIELD_LABEL_WIDTH)
            label.setFixedHeight(72)

        input_rows = (
            (self.horizontalLayout_2, self.input_001),
            (self.horizontalLayout_6, self.input_002),
            (self.horizontalLayout, self.input_003),
            (self.horizontalLayout_5, self.input_004),
            (self.horizontalLayout_3, self.input_005),
        )
        for row_layout, input_widget in input_rows:
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(12)
            row_layout.setStretch(0, 0)
            row_layout.setStretch(1, 1)
            input_widget.setObjectName('pathInput')
            input_widget.setStyleSheet('')
            input_widget.setMinimumHeight(72)
            input_widget.setMaximumHeight(77)

        self._simplify_button_row()
        self._fit_window_size()

    def _simplify_button_row(self):
        button_groups = (
            (self.frame_2, self.remove_suffix, 'dangerButton'),
            (self.frame_4, self.add_suffix, 'dangerButton'),
            (self.frame_6, self.modify_suffix, 'primaryButton'),
            (self.frame_8, self.bandizip, 'primaryButton'),
            (self.frame_13, self.bandizip_de, 'primaryButton'),
            (self.frame, self.delete_frame, 'primaryButton'),
            (self.frame_11, self.modify_name, 'primaryButton'),
        )
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(12)

        for frame, button, style_name in button_groups:
            self.horizontalLayout_4.removeWidget(frame)
            frame.setParent(None)
            button.setParent(self)
            button.setObjectName(style_name)
            button.setStyleSheet('')
            button.setMinimumWidth(0)
            button.setMinimumHeight(32)
            button.setMaximumSize(QSize(16777215, 16777215))
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            button.setCursor(Qt.PointingHandCursor)
            self.horizontalLayout_4.addWidget(button, 1)

    def _fit_window_size(self):
        self.adjustSize()
        compact_height = self.sizeHint().height()
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.resize(980, compact_height)
        self.setMinimumSize(860, compact_height)
        self.setMaximumHeight(compact_height)

    def init_view(self):
        self.remove_suffix.clicked.connect(self.remove_suffix_click)
        self.add_suffix.clicked.connect(self.auto_add_suffix_click)
        self.modify_suffix.clicked.connect(self.modify_suffix_click)
        self.bandizip.clicked.connect(self.bandizip_click)
        self.bandizip_de.clicked.connect(self.bandizip_de_click)
        self.delete_frame.clicked.connect(self.delete_frame_click)
        self.modify_name.clicked.connect(self.modify_name_click)

    def init_ui(self):
        data = database.get_json_data()
        if data:
            if "input_001_value" in data:
                self.input_001.setText(data["input_001_value"].replace("\n", ""))
            if "input_002_value" in data:
                self.input_002.setText(data["input_002_value"].replace("\n", ""))
            if "input_003_value" in data:
                self.input_003.setText(data["input_003_value"].replace("\n", ""))
            if "input_004_value" in data:
                self.input_004.setText(data["input_004_value"].replace("\n", ""))
            if "input_005_value" in data:
                self.input_005.setText(data["input_005_value"].replace("\n", ""))

    def get_input_value_list(self, log_file):
        self.input_001_value = utils.analysis_input_path(self.input_001)
        self.input_002_value = utils.analysis_input_path(self.input_002)
        self.input_003_value = utils.analysis_input_path(self.input_003)
        self.input_004_value = utils.analysis_input_path(self.input_004)
        self.input_005_value = utils.analysis_input_path(self.input_005)

        data = {
            'input_001_value': self.input_001_value,
            'input_002_value': self.input_002_value,
            'input_003_value': self.input_003_value,
            'input_004_value': self.input_004_value,
            'input_005_value': self.input_005_value
        }
        database.set_json_data(data)

        self.old_suffix = self.input_003_value
        if self.old_suffix and "." not in self.old_suffix:
            self.old_suffix = "." + self.old_suffix
        log_file.write("旧后缀：%s\n" % self.old_suffix)
        print("旧后缀：%s\n" % self.old_suffix)

        self.new_suffix = self.input_004_value
        if self.new_suffix and "." not in self.new_suffix:
            self.new_suffix = "." + self.new_suffix
        log_file.write("新后缀：%s\n" % self.new_suffix)
        print("新后缀：%s\n" % self.new_suffix)

        self.work_path = self.input_005_value
        log_file.write("工作路径：%s\n" % self.work_path)
        print("工作路径：%s\n" % self.work_path)

        log_file.write("\n\n")
        print("\n\n")

    def remove_suffix_click(self):
        log_file = open(path_ex.get_cache_path() + path_ex.LOG_REMOVE_SUFFIX, mode='w', encoding='utf-8')
        self.get_input_value_list(log_file)
        self.modify_suffix_task(self.work_path, "", "", log_file)
        log_file.close()
        show_result(self, self.remove_suffix.text(), '成功', kind='success')

    def auto_add_suffix_click(self):
        log_file = open(path_ex.get_cache_path() + path_ex.LOG_ADD_SUFFIX, mode='w', encoding='utf-8')
        self.get_input_value_list(log_file)
        self.auto_add_suffix_task(self.work_path, log_file)
        log_file.close()
        show_result(self, self.add_suffix.text(), '成功', kind='success')

    def modify_suffix_click(self):
        log_file = open(path_ex.get_cache_path() + path_ex.LOG_MODIFY_SUFFIX, mode='w', encoding='utf-8')
        self.get_input_value_list(log_file)
        if len(self.old_suffix) == 0 and len(self.new_suffix) == 0:
            show_result(
                self, self.modify_suffix.text(), '"旧后缀""新后缀"不能同时都为空', kind='info',
            )
            return

        self.modify_suffix_task(self.work_path, self.old_suffix, self.new_suffix, log_file)
        log_file.close()
        show_result(self, self.modify_suffix.text(), '成功', kind='success')

    def bandizip_click(self):
        self._start_zip_task(compress=True)

    def bandizip_de_click(self):
        self._start_zip_task(compress=False)

    def _set_zip_buttons_enabled(self, enabled):
        self.bandizip.setEnabled(enabled)
        self.bandizip_de.setEnabled(enabled)

    def _start_zip_task(self, compress):
        if self._zip_running:
            return

        log_name = path_ex.LOG_BANDIZIP if compress else path_ex.LOG_BANDIZIP_DE
        log_path = path_ex.get_cache_path() + log_name
        with open(log_path, 'w', encoding='utf-8') as log_file:
            self.get_input_value_list(log_file)

        button_title = self.bandizip.text() if compress else self.bandizip_de.text()
        if not self.work_path or not os.path.isdir(self.work_path):
            show_result(self, button_title, '请输入有效的工作路径', kind='warning')
            return

        subdirs = [
            name for name in os.listdir(self.work_path)
            if os.path.isdir(os.path.join(self.work_path, name))
        ]
        if not subdirs:
            show_result(self, button_title, '工作路径下没有子文件夹', kind='info')
            return

        self._zip_running = True
        self._zip_button_title = button_title
        self._set_zip_buttons_enabled(False)

        action_text = '压缩' if compress else '解压'
        self._zip_progress_dialog = ZipBusyDialog(action_text, len(subdirs), self)
        self._zip_progress_dialog.show()

        thread = threading.Thread(
            target=self._zip_worker,
            args=(compress, log_path, subdirs),
            daemon=True,
        )
        thread.start()

    def _zip_worker(self, compress, log_path, subdirs):
        success_count = 0
        skip_count = 0
        fail_count = 0
        total = len(subdirs)

        with open(log_path, 'a', encoding='utf-8') as log_file:
            for index, folder_name in enumerate(subdirs, start=1):
                old_file = os.path.join(self.work_path, folder_name)
                self.zip_progress_signal.emit(index, total, folder_name)

                if compress:
                    result = self._compress_folder(old_file, folder_name, log_file)
                else:
                    result = self._extract_folder(old_file, folder_name, log_file)

                if result == 'success':
                    success_count += 1
                elif result == 'skip':
                    skip_count += 1
                else:
                    fail_count += 1
                log_file.write('\n\n')

        action = '压缩' if compress else '解压'
        message = (
            f'{action}完成：成功 {success_count} 个，'
            f'跳过 {skip_count} 个，失败 {fail_count} 个'
        )
        if fail_count:
            message += '\n详情请查看日志'
        self.zip_done_signal.emit(fail_count == 0, message)

    def _compress_folder(self, old_file, folder_name, log_file):
        if utils.directory_has_zip(old_file):
            value = '%s 有zip文件不压缩' % old_file
            log_file.write('%s\n' % value)
            print('%s\n' % value)
            return 'skip'

        zip_path = utils.folder_zip_path(old_file, folder_name)
        try:
            utils.zip_directory(old_file, zip_path)
            value = '压缩 %s -> %s' % (old_file, zip_path)
            log_file.write('%s\n' % value)
            print('%s\n' % value)
        except Exception as e:
            value = '压缩失败 %s: %s' % (old_file, e)
            log_file.write('%s\n' % value)
            print('%s\n' % value)
            return 'fail'

        for file_name in os.listdir(old_file):
            file_path = os.path.join(old_file, file_name)
            if os.path.isfile(file_path) and not utils.is_zip_filename(file_name):
                log_file.write('删除文件 %s\n' % file_path)
                print('删除文件 %s\n' % file_path)
                os.remove(file_path)
        return 'success'

    def _extract_folder(self, old_file, folder_name, log_file):
        zip_path = utils.folder_zip_path(old_file, folder_name)
        if not os.path.isfile(zip_path):
            value = '%s 无zip文件不解压' % old_file
            log_file.write('%s\n' % value)
            print('%s\n' % value)
            return 'skip'

        for file_name in os.listdir(old_file):
            file_path = os.path.join(old_file, file_name)
            if os.path.isfile(file_path) and not utils.is_zip_filename(file_name):
                log_file.write('删除文件 %s\n' % file_path)
                print('删除文件 %s\n' % file_path)
                os.remove(file_path)

        try:
            utils.unzip_to_directory(zip_path, old_file)
            value = '解压 %s -> %s' % (zip_path, old_file)
            log_file.write('%s\n' % value)
            print('%s\n' % value)
            os.remove(zip_path)
            log_file.write('删除文件 %s\n' % zip_path)
            print('删除文件 %s\n' % zip_path)
            return 'success'
        except Exception as e:
            value = '解压失败 %s: %s' % (zip_path, e)
            log_file.write('%s\n' % value)
            print('%s\n' % value)
            return 'fail'

    def _on_zip_progress(self, current, total, folder_name):
        if not self._zip_progress_dialog:
            return
        self._zip_progress_dialog.set_progress(current, total, folder_name)

    def _on_zip_done(self, success, message):
        self._zip_running = False
        self._set_zip_buttons_enabled(True)
        if self._zip_progress_dialog:
            self._zip_progress_dialog.close()
            self._zip_progress_dialog = None
        show_zip_result(self, success, message, title=getattr(self, '_zip_button_title', ''))

    def delete_frame_click(self):
        log_file = open(path_ex.get_cache_path() + path_ex.LOG_DELETE_FRAME, mode='w', encoding='utf-8')
        self.get_input_value_list(log_file)
        if len(self.input_001_value) == 0:
            show_result(self, self.delete_frame.text(), '"旧文件名"不能为空', kind='info')
            return
        self.delete_frame_task(self.work_path, self.input_001_value, log_file)
        log_file.close()
        show_result(self, self.delete_frame.text(), '成功', kind='success')

    def modify_name_click(self):
        log_file = open(path_ex.get_cache_path() + path_ex.LOG_MODIFY_NAME, mode='w', encoding='utf-8')
        self.get_input_value_list(log_file)
        if len(self.input_001_value) == 0 or len(self.input_002_value) == 0:
            show_result(
                self, self.modify_name.text(), '"旧文件名""新文件名"不能为空', kind='info',
            )
            return
        self.modify_name_task(self.work_path, self.input_001_value, self.input_002_value, log_file)
        log_file.close()
        show_result(self, self.modify_name.text(), '成功', kind='success')

    def modify_suffix_task(self, dir_path, old_suffix, new_suffix, log_file):
        file_list = os.listdir(dir_path)
        for file in file_list:
            old_file = os.path.join(dir_path, file)
            if os.path.isdir(old_file):
                self.modify_suffix_task(old_file, old_suffix, new_suffix, log_file)
            else:
                if old_suffix:
                    new_file = old_file.replace(old_suffix, new_suffix)
                else:
                    portion = os.path.splitext(old_file)
                    if not portion[1]:
                        # 文件没有扩展名
                        new_file = os.path.join(dir_path, file + new_suffix)
                    else:
                        new_file = old_file.replace(portion[1], new_suffix)

                log_file.write("原始文件：%s\n" % old_file)
                print("原始文件：%s\n" % old_file)

                log_file.write("修改文件：%s\n" % new_file)
                print("修改文件：%s\n" % new_file)

                shutil.move(old_file, new_file)

    def auto_add_suffix_task(self, dir_path, log_file):
        file_list = os.listdir(dir_path)
        for file in file_list:
            old_file = os.path.join(dir_path, file)
            if os.path.isdir(old_file):
                self.auto_add_suffix_task(old_file, log_file)
            else:
                current_ext = os.path.splitext(file)[1]
                log_file.write("后缀名 = %s\n" % current_ext)
                print("后缀名 = %s\n" % current_ext)

                detected_ext = guess_file_extension(old_file)
                if detected_ext is None:
                    log_file.write("无法识别文件后缀：%s\n" % old_file)
                    print("无法识别文件后缀：%s\n" % old_file)
                    continue

                if current_ext and extensions_are_equivalent(current_ext, detected_ext):
                    log_file.write("后缀正确，跳过：%s\n" % old_file)
                    print("后缀正确，跳过：%s\n" % old_file)
                    continue

                if not current_ext:
                    log_file.write("后缀名空的文件 = %s\n" % old_file)
                    print("后缀名空的文件 = %s\n" % old_file)
                else:
                    log_file.write(
                        "后缀不正确：%s，识别为 %s\n" % (current_ext, detected_ext)
                    )
                    print("后缀不正确：%s，识别为 %s\n" % (current_ext, detected_ext))

                log_file.write("文件类型 = %s\n" % detected_ext)
                print("文件类型 = %s\n" % detected_ext)

                new_file = os.path.join(dir_path, file + detected_ext)

                log_file.write("原始文件：%s\n" % old_file)
                print("原始文件：%s\n" % old_file)

                log_file.write("修改文件：%s\n" % new_file)
                print("修改文件：%s\n" % new_file)

                shutil.move(old_file, new_file)

    def delete_frame_task(self, dir_path, filter_value, log_file):
        file_list = os.listdir(dir_path)
        for file in file_list:
            old_file = os.path.join(dir_path, file)
            if os.path.isdir(old_file):
                self.delete_frame_task(old_file, filter_value, log_file)
            else:
                if filter_value in file:
                    log_file.write("%s\n" % old_file)
                    print("%s\n" % old_file)
                    os.remove(old_file)

    def modify_name_task(self, dir_path, old_name, new_name, log_file):
        if not old_name or not new_name:
            return
        file_list = os.listdir(dir_path)
        for file in file_list:
            old_file = os.path.join(dir_path, file)
            if os.path.isdir(old_file):
                self.modify_name_task(old_file, old_name, new_name, log_file)
            else:
                if old_name in file:
                    new_file = os.path.join(dir_path, new_name)
                    log_file.write("旧文件 = %s\n" % old_file)
                    print("旧文件 = %s\n" % old_file)
                    log_file.write("新文件 = %s\n" % new_file)
                    print("新文件 = %s\n" % new_file)
                    shutil.move(old_file, new_file)
