import time
from test.ios_test.common.BaseWdaIOSPage import BaseWdaIOSPage
from utils.BaseDriver import Driver
from utils.BaseReadConfig import ReadConfig

# 页面元素 ---------------------------------
favourites_text = "Choose your favorite contents for a personalized experience"
skip_text = "SKIP"


class StartPage(BaseWdaIOSPage):

    def __init__(self, driver):
        super().__init__(driver)
        # self.logger.i("-------StartPage Object init----------")

    # @my_test_pages
    def start_interest_page(self):
        try:
            self.driver.alert.click("允许")
        except Exception as e:
            self.print(e)
        if self.exists(label=favourites_text):
            return True
        else:
            return False

    def start_interest_page_select(self):
        self.click_exists(timeout=5, label="Sports")
        self.click_exists(timeout=5, label="News")
        if self.info("enabled", label="NEXT") is True:
            self.click(label="NEXT")
            return True
        else:
            return False

    # @my_test_pages
    def start_interest_page_skip(self):
        self.click_exists(timeout=5, label=skip_text)
        if self.exists(name='topBar_logo') is True:
            return True
        else:
            return False


if __name__ == '__main__':
    rc = ReadConfig()
    d = Driver.init_ios_driver('184ed2e8e26199478f1e7c70605121c457877165')
    startPage = StartPage(d)
    startPage.start_interest_page()
    startPage.start_interest_page_select()
    print(startPage.start_interest_page_skip())
