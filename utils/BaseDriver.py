import uiautomator2 as u2
import wda
from appium import webdriver
from utils.BaseReadConfig import ReadConfig
from utils.BaseLog import Log

from utils.BaseDevicesInfo import get_android_version, get_ios_info

log_enabled = True


class Driver:

    @classmethod
    def init_driver(cls, device_or_ip):
        print(device_or_ip)
        logger = Log(device_or_ip, level='info')
        try:
            cls.d = u2.connect(device_or_ip)
            logger.i("{} connect to device! ".format(device_or_ip))
            return cls.d
        except Exception as e:
            logger.e("{} connect to device异常! {}".format(device_or_ip, e))
            # exit("connect to device异常")

    @classmethod
    def init_appium_driver(cls, device_or_ip):
        print(device_or_ip)
        rc = ReadConfig()
        logger = Log(device_or_ip, level='info')
        desired_capabilities = {
            "automationName": "Appium",
            "deviceName": device_or_ip,
            "platformName": "Android",
            "platformVersion": get_android_version(device_or_ip),
            "appPackage": rc.get_apk_name('IOS_StarTimesOn'),
            "appActivity": rc.get_app_start_activity(),
            "chromedriverExecutable": "G:/chromedriver/chromedriver960466445.exe",
            "enablePerformanceLogging": True,
            "unicodeKeyboard": True,
            "noReset": True,
            "newCommandTimeout": 6000,
            "dontStopAppOnReset": True
        }
        print(desired_capabilities)
        try:
            cls.appium_driver = webdriver.Remote(
                command_executor='http://127.0.0.1:4723/wd/hub',
                desired_capabilities=desired_capabilities
            )
            logger.i("{} connect to device! ".format(device_or_ip))
            return cls.appium_driver
        except Exception as e:
            logger.e("{} connect to device异常! {}".format(device_or_ip, e))

    @classmethod
    def get_driver(cls):
        return cls.d

    @classmethod
    def init_ios_driver(cls, device_or_ip):
        # print(device_or_ip)
        logger = Log(device_or_ip, level='info')
        try:
            cls.ios_driver = wda.USBClient(device_or_ip, port=8100)
            logger.i("{} connect to device! ".format(device_or_ip))
            return cls.ios_driver
        except Exception as e:
            logger.e("{} connect to device异常! {}".format(device_or_ip, e))
            # exit("connect to device异常")
        return cls.ios_driver

    @classmethod
    def init_appium_ios_driver(cls, device_or_ip, bundleId=None):
        print(device_or_ip)
        device_info = get_ios_info(device_or_ip)
        desired_capabilities = {
            "automationName": "XCUITest",
            "platformName": "iOS",
            "udid": device_or_ip,
            'platformVersion': device_info['ProductVersion'],
            'deviceName': device_info['DeviceName'],
            'noReset': True,
            # 没有以下三项appium就会找xcode。windows没有xcode，报错跑不下去
            "webDriverAgentUrl": "http://localhost:8200",
            "usePrebuiltWDA": True,
            "useXctestrunFile": False,
            "skipLogCapture": True,
        }
        if bundleId is not None:
            desired_capabilities["bundleId"] = bundleId
        print(desired_capabilities)
        logger = Log(device_or_ip, level='info')
        try:
            cls.appium_driver = webdriver.Remote(
                command_executor='http://127.0.0.1:4723/wd/hub',
                desired_capabilities=desired_capabilities
            )
            logger.i("{} connect to device! ".format(device_or_ip))
            return cls.appium_driver
        except Exception as e:
            logger.e("{} connect to device异常! {}".format(device_or_ip, e))

    # 静态方法类似普通方法，参数里面不用self。这些方法和类相关，
    # 但是又不需要类和实例中的任何信息、属性等等
    @staticmethod
    def static_foo():
        if log_enabled:
            print("log is enabled")
        else:
            print("log is disabled")


if __name__ == '__main__':
    Driver.init_driver(device='D511C1ZR62237866')
