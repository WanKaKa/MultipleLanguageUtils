# coding=utf-8
from appium import webdriver

desired_caps = {
    'platformName': 'Android',
    'platformVersion': '9.0',
    'deviceName': '联想K5 Pro',
    'appPackage': 'com.ddnapalon.calculator.gp',
    'appActivity': '.ScienceFragment',
    "automationName": "UiAutomator1"
}


def get_name(driver, name):
    """
    定位页面text元素
    :param driver:
    :param name:
    :return:
    """
    # element = driver.find_element_by_name(name)
    # return element
    element = driver.find_element_by_name(name)
    return element


def kevin():
    driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
    get_name(driver, "1").click()
    get_name(driver, "5").click()
    get_name(driver, "9").click()
    get_name(driver, "C").click()
    get_name(driver, "9").click()
    get_name(driver, "5").click()
    get_name(driver, "+").click()
    get_name(driver, "6").click()
    get_name(driver, "=").click()
    # driver.quit()


if __name__ == '__main__':
    kevin()
