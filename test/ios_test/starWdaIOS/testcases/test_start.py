# -*- coding: utf-8 -*-
import time

import allure
import pytest
import random
from test.ios_test.starWdaIOS.pages.StartPage import StartPage
from utils.BaseGlobalVar import GlobalVar


@pytest.fixture(scope="class")
def initStart(driver_setup):
    start_object = StartPage(driver_setup['driver'])
    # start_object.logger.i("----------start_object init-------------")
    yield start_object


@allure.feature("启动页测试")
@pytest.mark.run(order=10000)
class TestStart:
    condition = random.randint(0, 9)
    device_id = GlobalVar.get_value('device')

    @allure.title("启动页1010_欢迎页")
    @pytest.mark.run(order=10010)
    @pytest.mark.start
    @pytest.mark.smoke
    def test_start_welcome_page(self, initStart):
        time.sleep(2)
        if initStart.exists(labelContains='想给您发送通知'):
            initStart.logger.i(self.device_id + ": " + "启动页10010_欢迎页-成功")
            assert 0 == 0
        else:
            initStart.logger.i(self.device_id + ": " + "启动页10010_欢迎页-失败")
            assert 0 == 1

    @allure.title("启动页10020_兴趣页打开")
    @pytest.mark.run(order=10020)
    @pytest.mark.start
    @pytest.mark.smoke
    def test_start_interest_page(self, initStart):
        if initStart.start_interest_page():
            initStart.logger.i(self.device_id + ": " + "启动页10020_兴趣页打开-成功")
            assert 0 == 0
        else:
            initStart.logger.i(self.device_id + ": " + "启动页10020_兴趣页打开-失败")
            assert 0 == 1

    @allure.title("启动页10021_兴趣标签选择Sports、News")
    @pytest.mark.run(order=10021)
    @pytest.mark.start
    @pytest.mark.smoke
    @pytest.mark.skipif(condition % 2 == 0, reason="10021 和 10022 两者只能执行一个")
    def test_start_interest_page_select(self, initStart):
        if initStart.start_interest_page_select():
            initStart.logger.i(self.device_id + ": " + "启动页10021_兴趣标签选择Sports、News-成功")
            assert 0 == 0
        else:
            initStart.logger.i(self.device_id + ": " + "启动页10021_兴趣标签选择Sports、News-失败")
            assert 0 == 1

    @allure.title("启动页10022_兴趣标签跳过")
    @pytest.mark.run(order=10022)
    @pytest.mark.start
    @pytest.mark.skipif(condition % 2 == 1, reason="10021 和 10022 两者只能执行一个")
    def test_start_interest_page_skip(self, initStart):
        if initStart.start_interest_page_skip():
            initStart.logger.i(self.device_id + ": " + "启动页10022_兴趣标签跳过-成功")
            assert 0 == 0
        else:
            initStart.logger.i(self.device_id + ": " + "启动页10022_兴趣标签跳过-失败")
            assert 0 == 1


if __name__ == '__main__':
    testStart = TestStart()
    testStart.test_start_welcome_page()
