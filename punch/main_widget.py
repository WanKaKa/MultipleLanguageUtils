from PyQt5.QtWidgets import QWidget, QMessageBox

import time
import threading
import os
import numpy
import cv2

from punch import utils
from punch import main_ui


class Image:
    def __init__(self, image):
        self.image = cv2.imread(image, cv2.COLOR_RGB2BGR)

    @property
    def width(self):
        return self.image.shape[1]

    @property
    def height(self):
        return self.image.shape[0]


class MatchImg(object):
    def __init__(self, source, template, threshold=0.95):
        """
        匹配一个图片，是否是另一个图片的局部图。source是大图，template是小图。即判断小图是否是大图的一部分。
        :param source:
        :param template:
        :param threshold: 匹配程度，值越大，匹配程度要求就越高，最好不要太小
        """
        self.source_img = source
        self.template_img = template
        self.threshold = threshold

    def match_template(self, method=cv2.TM_CCOEFF_NORMED):
        """
        返回小图左上角的点，在大图中的坐标。
        :param method:
        :return: list[tuple(x,y),...]
        """
        result = cv2.matchTemplate(self.source_img.image, self.template_img.image, method)
        locations = numpy.where(result >= self.threshold)
        res = list(zip(locations[1], locations[0]))  # 返回的是匹配到的template左上角那个坐标点在image中的位置，可能有多个值
        return res

    def get_template_position(self):
        """
        获取小图在大图中，左上角和右下角的坐标
        :return: List[list[x,y,x,y],...]
        """
        res = self.match_template()
        new_pos = []
        for r in res:
            r = list(r)
            r.append(r[0] + self.template_img.width)
            r.append(r[1] + self.template_img.height)
            new_pos.append(r)
        return new_pos

    def get_img_center(self):
        """
        获取大图中，每个小图中心点所在的坐标
        :return:
        """
        pos = self.match_template()
        points = []
        for p in pos:
            x, y = p[0] + int(self.template_img.width / 2), p[1] + int(self.template_img.height / 2)
            points.append((x, y))
        return points


class MainWidget(QWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self.ui = main_ui.Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle("爽歪歪")

        self.screenshot_image_1 = "C:/IJoySoft/Kevin/AutoPunch/AutoPunchScreenshot_1.png"
        self.mate_punch_list_1 = {
            "app.png",
        }
        self.screenshot_image_2 = "C:/IJoySoft/Kevin/AutoPunch/AutoPunchScreenshot_2.png"
        self.mate_punch_list_2 = {
            "punch.png",
            "punch_2.png",
            "punch_3.png"
        }
        self.screenshot_image_3 = "C:/IJoySoft/Kevin/AutoPunch/AutoPunchScreenshot_3.png"
        self.mate_punch_list_3 = {
            "punch_complete.png",
            "punch_complete_2.png",
        }

        self.timing_hour = 20
        self.timing_minutes = 0
        self.countdown = 0
        self.punch_time = 0
        self.break_timer = False

        self.ui.hour.setText(str(self.timing_hour))
        self.ui.ok.clicked.connect(lambda: self.start_countdown(False))
        self.ui.ok_now.clicked.connect(lambda: self.start_countdown(True))

    def start_countdown(self, running_now=False):
        if not self.ui.hour.text().isdigit() or not self.ui.minutes.text().isdigit():
            QMessageBox.information(self, '提示', "请输入数字")
            return

        # 获取输入的时间
        self.timing_hour = int(self.ui.hour.text())
        self.timing_minutes = int(self.ui.minutes.text())
        self.get_countdown(running_now)

        timer = threading.Timer(1, function=lambda: self.countdown_task(running_now))
        timer.start()

    def get_countdown(self, running_now=False):
        # 获取电脑当前时间
        current_time = time.localtime(time.time())
        current_hour = int(time.strftime('%H', current_time))
        current_minutes = current_hour * 60 + int(time.strftime('%M', current_time))
        current_second = current_minutes * 60 + int(time.strftime('%S', current_time))

        timing_second = self.timing_hour * 3600 + self.timing_minutes * 60
        if running_now:
            self.countdown = 0
        else:
            if timing_second <= current_second:
                if abs(timing_second - current_second) <= 5:
                    self.countdown = 0
                else:
                    self.countdown = 24 * 3600 + timing_second - current_second
            else:
                self.countdown = timing_second - current_second

    def countdown_task(self, running_now=False):
        if self.countdown <= 0:
            self.ui.countdown.setText("开始表演")
            timer = threading.Timer(1, function=self.punch_task)
            timer.start()
            return
        self.get_countdown(running_now)

        countdown_minutes, countdown_second = divmod(self.countdown, 60)
        countdown_hour, countdown_minutes = divmod(countdown_minutes, 60)
        self.ui.countdown.setText("%02d:%02d:%02d" % (countdown_hour, countdown_minutes, countdown_second))

        if self.break_timer:
            print("倒计时任务终止")
            return
        timer = threading.Timer(1, function=lambda: self.countdown_task(running_now))
        timer.start()

    def punch_task(self):
        if self.punch_time == 0:
            self.ui.countdown.setText("步骤一 截图中")
            screenshot(self.screenshot_image_1)
            self.ui.countdown.setText("步骤一 截图完成")
        elif self.punch_time == 10:
            self.mate_punch_1()
        elif self.punch_time == 30:
            self.ui.countdown.setText("步骤二 截图中")
            screenshot(self.screenshot_image_2)
            self.ui.countdown.setText("步骤二 截图完成")
        elif self.punch_time == 40:
            self.mate_punch_2()
        elif self.punch_time == 60:
            self.ui.countdown.setText("步骤三 截图中")
            screenshot(self.screenshot_image_3)
            self.ui.countdown.setText("步骤三 截图完成")
        elif self.punch_time == 70:
            self.mate_punch_3()

            print("表演终止")
            return

        if self.break_timer:
            print("表演终止")
            return

        self.punch_time += 1
        timer = threading.Timer(1, self.punch_task)
        timer.start()

    def mate_punch_1(self):
        screenshot_image = Image(self.screenshot_image_1)
        for file_name in self.mate_punch_list_1:
            if self.mate_punch_image(screenshot_image, file_name):
                return
        self.ui.countdown.setText("步骤一 无点击 截图中等待中")

    def mate_punch_2(self):
        screenshot_image = Image(self.screenshot_image_2)
        for file_name in self.mate_punch_list_2:
            if self.mate_punch_image(screenshot_image, file_name):
                return
        self.ui.countdown.setText("步骤二 无点击 截图中等待中")

    def mate_punch_3(self):
        screenshot_image = Image(self.screenshot_image_3)
        for file_name in self.mate_punch_list_3:
            if self.mate_punch_image(screenshot_image, file_name):
                return
        self.ui.countdown.setText("步骤三 无点击")

    def mate_punch_image(self, screenshot_image: Image, file_name):
        image_mate = Image(utils.resource_path(os.path.join("image", file_name)))
        process = MatchImg(screenshot_image, image_mate, 0.8)
        points = process.get_img_center()
        if len(points) > 0:
            self.ui.countdown.setText("点击(%d, %d)" % (points[0][0], points[0][1]))
            print(points)
            os.system("adb shell input tap %d %d" % (points[0][0], points[0][1]))
            return True
        return False

    def closeEvent(self, event):
        self.break_timer = True


def screenshot(file_path):
    os.system("adb shell screencap /sdcard/AutoPunchScreenshot.png")
    os.system("adb pull /sdcard/AutoPunchScreenshot.png %s" % file_path)
