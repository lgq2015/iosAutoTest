import allure
import pytest
from test.ios_test.starWdaIOS.pages.LoginPage import LoginPage
from utils.BaseReadConfig import ReadConfig
from utils.BaseGlobalVar import GlobalVar

rc = ReadConfig()


# init（）写在这里的好处 只需要初始化一次


@pytest.fixture(scope="class")
def initLogin(driver_setup):
    login_object = LoginPage(driver_setup['driver'])
    # login_object.logger.i("----------login_object init-------------")
    yield login_object


# @pytest.mark.usefixtures('driver_setup') 无法取得返回值
@allure.feature("登录模块")
@pytest.mark.run(order=20000)
class TestLogin:
    device_id = GlobalVar.get_value('device')

    @allure.title("登录20010_点击SIGN IN")
    @pytest.mark.run(order=20010)
    @pytest.mark.login
    @pytest.mark.smoke
    @pytest.mark.skip(reason="每个登录里面调用，此处不再单独测试")
    def test_signin_entry(self, initLogin):
        if initLogin.signin_entry():
            initLogin.logger.i(self.device_id + ": " + "登录20010_点击SIGN IN-成功")
            assert 0 == 0
        else:
            initLogin.logger.i(self.device_id + ": " + "登录20010_点击SIGN IN-失败")
            assert 0 == 1

    @allure.title("登录20011_手机账号登录操作")
    @pytest.mark.run(order=20011)
    @pytest.mark.login
    @pytest.mark.smoke
    @pytest.mark.flaky(reruns=1, reruns_delay=2)
    def test_signin_phone_login(self, initLogin):
        login_name_phone = rc.cf.get('Account', 'login_name_phone')
        password_phone = rc.cf.get('Account', 'password_phone')
        if initLogin.signin_phone_login(login_name_phone, password_phone):
            initLogin.logger.i(self.device_id + ": " + "登录20011_手机账号登录操作-成功")
            assert 0 == 0
        else:
            initLogin.logger.i(self.device_id + ": " + "登录20011_手机账号登录操作-失败")
            assert 0 == 1

    @allure.title("登录20012_手机账号历史登录操作")
    @pytest.mark.run(order=20012)
    @pytest.mark.login
    @pytest.mark.smoke
    def test_signin_phone_history_login(self, initLogin):
        login_name_phone = rc.cf.get('Account', 'login_name_phone')
        if initLogin.signin_phone_history_login(login_name_phone):
            initLogin.logger.i(self.device_id + ": " + "登录20012_手机账号历史登录操作-成功")
            assert 0 == 0
        else:
            initLogin.logger.i(self.device_id + ": " + "登录20012_手机账号历史登录操作-失败")
            assert 0 == 1

    @allure.title("登录20020_邮箱账号登录操作")
    @pytest.mark.run(order=20020)
    @pytest.mark.login
    @pytest.mark.smoke
    @pytest.mark.flaky(reruns=1, reruns_delay=2)
    def test_signin_email_login(self, initLogin):
        login_name_email = rc.cf.get('Account', 'login_name_email')
        password_email = rc.cf.get('Account', 'password_email')
        if initLogin.signin_email_login(login_name_email, password_email):
            initLogin.logger.i(self.device_id + ": " + "登录2020_邮箱账号登录操作-成功")
            assert 0 == 0
        else:
            initLogin.logger.i(self.device_id + ": " + "登录2020_邮箱账号登录操作-失败")
            assert 0 == 1

    @allure.title("登录20021_邮箱账号历史登录操作")
    @pytest.mark.run(order=20021)
    @pytest.mark.login
    @pytest.mark.smoke
    def test_signin_email_history_login(self, initLogin):
        login_name_email = rc.cf.get('Account', 'login_name_email')
        if initLogin.signin_email_history_login(login_name_email):
            initLogin.logger.i(self.device_id + ": " + "登录2021_邮箱账号历史登录操作-成功")
            assert 0 == 0
        else:
            initLogin.logger.i(self.device_id + ": " + "登录2021_邮箱账号历史登录操作-失败")
            assert 0 == 1

    @allure.title("登录20050_账号退出操作")
    @pytest.mark.run(order=20050)
    @pytest.mark.login
    # @pytest.mark.skip(reason="先不退出")
    def test_logout(self, initLogin):
        if initLogin.logout():
            initLogin.logger.i(self.device_id + ": " + "登录20050_账号退出操作-成功")
            assert 0 == 0
        else:
            initLogin.logger.i(self.device_id + ": " + "登录20050_账号退出操作-失败")
            assert 0 == 1


if __name__ == '__main__':
    testLogin = TestLogin()
    testLogin.test_signin_entry()
