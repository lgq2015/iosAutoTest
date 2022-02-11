import multiprocessing
import time
from test.ios_test.common.BaseWdaIOSPage import BaseWdaIOSPage
from utils.BaseDevicesInfo import get_ios_devices_list
from utils.BaseDriver import Driver
from utils.BaseReadConfig import ReadConfig

# 页面元素 ---------------------------------
pack_version = ReadConfig().get_apk_name('IOS_StarTimesOn')
ll_play = pack_version + ":id/ll_play"
ll_me = pack_version + ":id/ll_me"


class HomePage(BaseWdaIOSPage):

    def __init__(self, driver):
        super().__init__(driver)
        # self.logger.i("-------HomePage Object init----------")

    # 返回到根目录LiveTV页方法
    def back_to_live_tv(self):
        while True:
            if self.driver(resourceId=ll_play).exists(timeout=2) is False:
                self.driver.press("back")
            else:
                self.driver(resourceId=ll_play).click()
                break


def run_case(device):
    d = Driver.init_ios_driver(device)
    homepage = HomePage(d)
    homepage.app_start("cn.10086.app")
    homepage.exists(label="每日签到")
    homepage.click_exists(name="账单查询")


if __name__ == '__main__':
    rc = ReadConfig()
    device_list = ['184ed2e8e26199478f1e7c70605121c457877165']
    device_list = get_ios_devices_list()
    with multiprocessing.Pool(len(device_list)) as pool:
        pool.map(run_case, device_list)
