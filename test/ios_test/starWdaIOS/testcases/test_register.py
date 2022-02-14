import allure
import pytest
from pytest_assume.plugin import assume

from model.RegisterModel import RegisterModel
from test.ios_test.starWdaIOS.pages.RegisterPage import RegisterPage
from utils.BaseReadConfig import ReadConfig
from utils.BaseGlobalVar import GlobalVar

rc = ReadConfig()


@pytest.fixture(scope="class")
def initRegister(driver_setup):
    register_object = RegisterPage(driver_setup['driver'])
    # login_object.logger.i("----------login_object init-------------")
    yield register_object


@allure.feature("注册模块")
@pytest.mark.run(order=20100)
class TestRegister:
    device_id = GlobalVar.get_value('device')

    @allure.title("注册20110_手机号注册")
    @pytest.mark.run(order=20110)
    @pytest.mark.register
    @pytest.mark.smoke
    def test_phone_register(self, initRegister):
        register_phone = rc.cf.get('Account', 'register_phone')
        password_phone = rc.cf.get('Account', 'register_password_phone')
        output_data = initRegister.phone_register(register_phone, password_phone)
        pytest.assume(True, output_data['phone_exits'])
        pytest.assume(True, output_data['tip_sign_in'])
        with assume:  # 两种写法使用上下文管理器的好处是不用显示去try和finally捕获异常
            assert output_data['message_send'], '手机验证码发送失败'
        with assume:
            assert output_data['message_fault_valid'], '输入错误的验证码未通过'
        with assume:
            assert output_data['message_right_valid'], '输入正确的验证码未通过'
        with assume:
            assert output_data['password_short_valid']
        with assume:
            assert output_data['password_long_valid']
        with assume:
            assert output_data['password_same_valid']
        with assume:
            assert output_data['password_pass']
        with assume:
            assert output_data['register_pass']
        if output_data['register_pass']:
            initRegister.logger.i(self.device_id + ": " + "注册20110_手机号注册操作-成功")
            RegisterModel().del_phone_register(register_phone)
        else:
            initRegister.logger.i(self.device_id + ": " + "注册20110_手机号注册操作-失败")

    @allure.title("注册20120_邮箱注册")
    @pytest.mark.run(order=20120)
    @pytest.mark.register
    @pytest.mark.smoke
    @pytest.mark.flaky(reruns=1, reruns_delay=2)
    def test_email_register(self, initRegister):
        register_email = rc.cf.get('Account', 'register_email')
        password_email = rc.cf.get('Account', 'register_password_email')
        output_data = initRegister.email_register(register_email, password_email)
        pytest.assume(True, output_data['email_suffix'])
        pytest.assume(True, output_data['email_exits'])
        pytest.assume(True, output_data['tip_sign_in'])
        pytest.assume(True, output_data['message_send'])
        pytest.assume(True, output_data['message_fault_valid'])
        pytest.assume(True, output_data['message_right_valid'])
        pytest.assume(True, output_data['password_short_valid'])
        pytest.assume(True, output_data['password_long_valid'])
        pytest.assume(True, output_data['password_same_valid'])
        pytest.assume(True, output_data['password_pass'])
        pytest.assume(True, output_data['register_pass'])
        if output_data['register_pass']:
            initRegister.logger.i(self.device_id + ": " + "注册20120_邮箱注册操作-成功")
            RegisterModel().del_email_register(register_email)
        else:
            initRegister.logger.i(self.device_id + ": " + "注册20120_邮箱注册操作-失败")


if __name__ == '__main__':
    testRegister = TestRegister()
    # testRegister.test_phone_register()
    testRegister.test_email_register()
