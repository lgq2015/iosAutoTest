import time

import allure
from test.ios_test.common.BaseWdaIOSPage import BaseWdaIOSPage
from utils.BaseDriver import Driver
from utils.BaseReadConfig import ReadConfig

# 页面元素 ---------------------------------
pack_version = ReadConfig().get_apk_name('IOS_StarTimesOn')
resource_id = pack_version + ":id/"

bottom_menu = {
    'home':  "Home",
    'live_tv': "Live TV",
    'me': "Me"
}
credential_save_confirm = "com.google.android.gms:id/credential_save_confirm"
autofill_save = 'android:id/autofill_save'
gps_cancle = resource_id + "iv_gps_cancel"
actionbar_title = resource_id + "tv_actionbar_title"
dialog_later = resource_id + "dialog_later"


class PublicWdaIOSPage(BaseWdaIOSPage):

    def __init__(self, driver):
        super().__init__(driver)
        # self.logger.i("-------HomePage Object init----------")

    # 点击底部栏
    def click_bottom_menu(self, bottomName='me'):
        label_text = bottom_menu[bottomName]
        while True:
            time.sleep(1)
            if self.exists(label=label_text) is False:
                self.click_exists(2, labelContains="back")
            else:
                self.click(label=label_text)
                break

    # 关闭一些弹窗
    def window_close(self):
        # gps定位弹窗
        # self.click_gone(2, resourceId=gps_cancle)
        pass


if __name__ == '__main__':
    rc = ReadConfig()
    d = Driver.init_ios_driver('184ed2e8e26199478f1e7c70605121c457877165')
    print(d.device_info)
    print(d.serial)
    publicPage = PublicPage(d)
