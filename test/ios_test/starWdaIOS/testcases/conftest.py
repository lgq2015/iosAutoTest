import pytest
import time

from test.ios_test.common.BaseWdaIOSPage import BaseWdaIOSPage
from utils.BaseDriver import Driver
from utils.BaseLog import Log
from utils.BaseReadConfig import ReadConfig


# 定义命令行传参参数device 设备序列号
def pytest_addoption(parser):
    parser.addoption("--device", action="store", default="22932a78f00d7ece", help="None")


# 命令行参数传递给pytest
@pytest.fixture(scope="session")
def device(request):
    return request.config.getoption("--device")


# 初始化开始连接设备
@pytest.fixture(scope="session")
def driver_setup(device):
    logger = Log(filename=device, level='info')
    logger.i("-------初始化driver-----------")
    driver = Driver.init_ios_driver(device)
    time.sleep(10)
    base = BaseWdaIOSPage(driver)

    rc = ReadConfig()
    apk_name = rc.get_apk_name('IOS_StarTimesOn')
    logger.i(f"-------清除app:{apk_name}-----------")
    # base.app_clear(apk_name)
    # time.sleep(5)

    logger.i(f"-------启动app:{apk_name}-----------")
    base.app_start(apk_name)

    return_dict = {
        # 'base': base,
        'driver': driver,
        # 'logger': logger
    }
    yield return_dict

    logger.i("-------关闭app-----------")
    # driver.app_stop(apk_name)
