import hashlib
import subprocess
import time
import os
import re

import tidevice
from tidevice._device import BaseDevice
from utils import BaseDevicesInfo
from utils.BaseLog import Log
from utils.BaseReadConfig import ReadConfig
from utils.BaseInitPath import InitPath
from utils.BaseDriver import Driver
from selenium import webdriver

rc = ReadConfig()


class BaseWdaIOSPage(object):
    all_elements = {}

    def __init__(self, driver: object) -> object:
        self.udid = driver.info['name']
        self.logger = Log(filename=self.udid, level='info')
        self.driver = driver

    def print(self, *args):
        # print(sys._getframe().f_code.co_name)
        # print(sys._getframe().f_back.f_code.co_name)
        print(self.udid, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), *args)

    # 返回chrome driver
    def chromeDriver(self, serial, package):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('androidDeviceSerial', serial)
        options.add_experimental_option('androidPackage', package)
        options.add_experimental_option('androidUseRunningApp', True)
        # options.add_experimental_option('androidActivity', '.activity.BrowserActivity')
        chrome_driver_name = 'chromedriver' + BaseDevicesInfo.get_app_version('com.google.android.webview')
        chrome_driver_name = chrome_driver_name.replace('.', '')
        # print(chrome_driver_name)
        return webdriver.Chrome(chrome_driver_name, options=options)

    def long_click(self, **kw):
        self.element(**kw).long_click()

    def element(self, **kw):
        key = hashlib.md5((self.udid + str(kw)).encode(encoding='UTF-8')).hexdigest()
        el = self.all_elements.get(key)
        self.print('元素: ' + str(kw))
        if el is None:
            el = self.all_elements[key] = self.driver(**kw)
        return el

    # 在timeout 时间里检测某个元素是否存在
    def wait_exists(self, timeout=0, **kw):
        def wait_handle():
            start_time = time.time()
            while time.time() - start_time < timeout:
                if self.exists(**kw):
                    return True
                time.sleep(0.5)
            return False

        result = wait_handle()
        self.print('等待了{0}s后返回exists状态的结果:{1}'.format(timeout, result))
        return result

    def exists(self, **kw):
        exist = self.driver(**kw).exists
        self.print('%s exists 结果:' % str(kw), exist)
        return exist

    def click(self, **kw):
        self.element(**kw).click()
        self.print('%s click Action' % str(kw))

    def element_center(self, **kw):
        lx, ly, rx, ry = self.element_bounds(**kw)
        return int(lx + rx // 2), int(ly + ry // 2)

    def element_bounds(self, **kw):
        scale = 1  # self.driver.scale
        lx, ly, rx, ry = self.element(**kw).bounds
        return lx * scale, ly * scale, rx * scale, ry * scale

    def click_offset(self, offset=(0.5, 0.5), **kw):
        lx, ly, rx, ry = self.driver(**kw).bounds
        self.print('元素坐标 (%d,%d) ,元素长宽 (%d,%d)' % (lx, ly, rx, ry))
        if offset is None:
            offset = (0.5, 0.5)  # default center
        xoff, yoff = offset
        x = lx + rx * xoff
        y = ly + ry * yoff
        self.print('元素偏移后坐标 (%d,%d)' % (x, y))
        self.driver.click(int(x), int(y))

    def click_outer_offset(self, offset=(0, 0), **kw):
        lx, ly, rx, ry = self.driver(**kw).bounds
        self.print('元素坐标 (%d,%d)' % (lx, ly))
        xoff, yoff = offset
        x = lx + xoff
        y = ly + yoff
        self.print('元素偏移后坐标 (%d,%d)' % (x, y))
        self.driver.click(int(x), int(y))

    def set_text(self, text, **kw):
        self.click(**kw)
        self.driver.send_keys(text)

    def clear_text(self, **kw):
        self.element(**kw).clear_text()

    def click_gone(self, maxretry=1, interval=1.0, **kw):
        self.print('%s click_gone Action' % str(kw))
        self.click_exists(**kw)
        while maxretry > 0:
            time.sleep(interval)
            if not self.exists(**kw):
                return True
            self.click_exists(**kw)
            maxretry -= 1
        return False

    def click_exists(self, timeout=0, **kw):
        click_rs = self.element(**kw).click_exists(timeout=timeout)
        self.print('%s click_exists Action:' % str(kw), click_rs)
        return click_rs

    def scroll(self, direction='visible', distance=1.0, **kw):
        if direction == 'visible':
            self.element(**kw).scroll(direction)
        else:
            self.element(**kw).scroll(direction, distance)
        time.sleep(3)

    def xpath_element(self, xpath):
        key = hashlib.md5((self.udid + xpath).encode(encoding='UTF-8')).hexdigest()
        el = self.all_elements.get(key)
        self.print('查找元素: ' + xpath)
        if el is None:
            el = self.all_elements[key] = self.driver.xpath(xpath)
        return el

    def xpath_wait(self, xpath, timeout=100):
        result = self.xpath_element(xpath).wait(timeout=timeout)
        self.print('等待了{0}s后返回exists状态的结果:{1}'.format(timeout, result))
        return result

    def xpath_exists(self, xpath=''):
        exist = self.xpath_element(xpath).exists
        self.print('%s xpath_exists 结果:' % xpath, exist)
        return exist

    def xpath_click(self, timeout=0, xpath=''):
        self.xpath_element(xpath).click(timeout=timeout)
        self.print('%s xpath_click Action' % xpath)

    def xpath_click_exists(self, timeout=0, xpath=''):
        click_rs = self.xpath_element(xpath).click_exists(timeout=timeout)
        self.print('%s xpath_click_exists Action:' % xpath, click_rs)
        return click_rs

    # 滚动
    def xpath_scroll(self, direction='forward', xpath=''):
        self.xpath_element(xpath).scroll(direction)

    def xpath_info(self, xpath, column=None):
        if column is None:
            return self.driver.xpath(xpath).info
        else:
            return self.driver.xpath(xpath).info[column]

    def info(self, column=None, **kw):
        e = self.element(**kw).get(timeout=10.0)
        if column is None:
            return e
        else:
            var = 'e.' + column
            return eval(var)

    # 安装apk包
    def app_is_install(self, apk_name):
        pi = subprocess.Popen("tidevice applist", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        app_list = pi.stdout.read().decode('utf-8')
        # print(app_list)
        if apk_name in app_list:
            return True
        else:
            return False

    # 安装apk包
    def app_install_ipa(self, apk_name):
        if not self.app_is_install(apk_name):
            apk_path = InitPath.get_data_path(apk_name + '.ipa')
            if not os.path.exists(apk_path):
                raise Exception("ipa file not exist")
                # sys.exit(0)
            else:
                self.logger.i(f'ipa install from path : {apk_path}')
                BaseDevice().app_install(apk_path)
                self.logger.i('ipa install success')
        else:
            pass
            self.logger.i('ipa have be installed')

    # 卸载ipa包
    def app_uninstall_ipa(self, apk_name):
        if self.app_is_install(apk_name):
            BaseDevice().app_uninstall(bundle_id=apk_name)

    # 启动app
    def app_start(self, apk_name):
        self.driver.app_start(apk_name)

    # 关闭app
    def app_stop(self, apk_name):
        self.driver.app_stop(apk_name)

    # 获取前台应用 package, activity
    def app_current(self, column=None):
        if column is not None:
            return self.driver.app_current()[column]
        return self.driver.app_current()

    def app_clear(self, apk_name):
        self.app_uninstall_ipa(apk_name)
        self.app_install_ipa(apk_name)


if __name__ == '__main__':
    d = Driver.init_ios_driver('184ed2e8e26199478f1e7c70605121c457877165')
    base = BaseWdaIOSPage(d)
    print(base.app_is_install('com.startimes.onlinetv'))
