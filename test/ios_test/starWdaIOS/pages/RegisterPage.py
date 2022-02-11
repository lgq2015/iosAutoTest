import multiprocessing
from test.ios_test.starWdaIOS.pages.LoginPage import LoginPage
from test.ios_test.common.PublicWdaIOSPage import PublicWdaIOSPage
from utils.BaseDevicesInfo import get_ios_devices_list
from utils.BaseDriver import Driver
from utils.BaseReadConfig import ReadConfig
from model.RegisterModel import RegisterModel
import time

rc = ReadConfig()

# 页面元素 ---------------------------------
pack_version = ReadConfig().get_apk_name('IOS_StarTimesOn')
resource_id = pack_version + ":id/"
dialog_confirm = "OK"
register_mobile_area_tv = "ic_arrow"
iv_area_name = resource_id + "iv_area_name"
tv_next = resource_id + "tv_next"
textinput_error = "The account exists. Sign in"
iv_edit = resource_id + "iv_edit"
tv_information = resource_id + "tv_information_email"
tv_create_account = "No account？Register"
tv_phone = "Phone Number"
tv_email = "Email Address"
et_custom_password = resource_id + "et_custom_password"
btn_send_verify_code_register = "GET CODE"
btn_send_email_code_register = "GET CODE"
tv_error_hint = resource_id + "tv_error_hint"
tv_register_check_next = "NEXT"
tv_set_login_pwd_next = resource_id + "tv_set_login_pwd_next"
tv_code_sent = resource_id + "tv_code_sent"
til_country_code = resource_id + "til_country_code"
tv_next = resource_id + "tv_next"
tv_mailbox_name = resource_id + "tv_mailbox_name"
yan_zheng_ma = '//Window[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[3]/Other[2]'
shouji_yan_zheng_ma = '//Window[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[3]/Other[3]'


class RegisterPage(PublicWdaIOSPage):

    def __init__(self, driver):
        super().__init__(driver)
        self.login = LoginPage(driver)

    # 手机注册
    def phone_register(self, register_phone, password_phone):
        output_data = {'phone_exits': False, 'message_send': False, 'message_fault_valid': False,
                       'message_right_valid': False, 'password_short_valid': False, 'password_long_valid': False,
                       'password_same_valid': False, 'password_pass': False, 'register_pass': False}
        self.login.signin_entry()
        self.login.history_login(isRemove=True)
        self.click_offset(offset=(0.8, 0.5), label=tv_create_account)  # # 点击注册
        self.click_exists(2, label=tv_phone)  # 点击手机号注册
        self.click_exists(2, name=register_mobile_area_tv)  # 切换国家
        self.click_exists(5, label="Nigeria")  # 切换Niger
        self.click_exists(2, className="TextField")  # 点击手机号输入框
        self.driver.send_keys(rc.cf.get('Account', 'login_name_phone'))  # 输入存在的手机号
        self.click_exists(2, label=btn_send_verify_code_register)  # 点击发送验证码
        self.click_exists(2, label=dialog_confirm)  # 确认发送短信
        time.sleep(3)
        # 校验存在过的手机号
        if self.exists(label='The account exists. Sign in'):
            print("账号存在校验显示成功")
            output_data['phone_exits'] = True
        time.sleep(3)
        self.clear_text(className="TextField")  # 先清空内容
        self.driver.send_keys(register_phone)  # 输入没有注册过的手机号
        self.click_exists(2, label=btn_send_verify_code_register)  # 点击发送验证码
        self.click_exists(2, label=dialog_confirm)  # 确认发送短信
        time.sleep(8)
        if self.exists(label='The verification code has been sent to your phone.'):
            print("验证码发送成功")
            output_data['message_send'] = True
            self.xpath_click_exists(2, xpath=shouji_yan_zheng_ma)
            for shu in '0000':
                self.click(label=shu)  # 输入错误验证码
            time.sleep(3)
            if self.exists(label='This code you entered is incorrect. Please try again.'):
                print("错误验证码校验成功")
                output_data['message_fault_valid'] = True
                self.xpath_click_exists(2, xpath=shouji_yan_zheng_ma)  # 点击验证码输入框
                for i in range(4):
                    self.click(label='Delete')  # 删除错误验证码
            time.sleep(3)
            # 获取数据库验证码
            data = RegisterModel().get_sms_code(register_phone)
            yzm_right = data['code']
            for i in yzm_right:
                self.click(label=i)  # 输入正确验证码
            time.sleep(3)
            if self.exists(label="Set Password"):  # ios验证码正确后直接跳转到下一页了
                print("正确验证码校验成功")
                output_data['message_right_valid'] = True

            self.click(label='register see', index=1)
            self.click(className='TextField', index=1)  # 点击第一个密码输入框
            short_password = "12345"
            self.driver.send_keys(short_password)  # 输入特别短的密码

            self.click(label='register see', index=2)
            self.click(className='TextField', index=2)  # 点击确认密码输入框
            self.driver.send_keys(short_password)  # 输入特别短的密码
            self.click_exists(label='NEXT')
            time.sleep(3)
            if self.exists(label='The password can not be less than 6 characters!'):
                print("短密码校验成功")
                output_data['password_short_valid'] = True

            long_password = "12345678912345678910"
            self.clear_text(className='TextField', index=1)  # 清空第一个密码输入框内容
            self.driver.send_keys(long_password)  # 输入特别长的密码
            self.click_exists(label='NEXT')
            time.sleep(3)
            if self.info('text', label='The password can not be more than 18 letters!'):
                print("长密码校验成功")
                output_data['password_long_valid'] = True

            self.clear_text(className='TextField', index=1)  # 清空第一个密码输入框内容
            self.driver.send_keys(password_phone)  # 输入格式正确的密码

            self.clear_text(className='TextField', index=2)  # 清空第二个密码输入框内容
            reverse_password = password_phone[::-1]
            self.driver.send_keys(reverse_password)  # 输入不一致的密码
            self.click_exists(2, label='NEXT')  # 点击下一步next
            time.sleep(3)
            if self.exists(label='The two passwords you entered did not match'):
                print("密码不一致校验成功")
                output_data['password_same_valid'] = True

            self.clear_text(className='TextField', index=2)  # 清空确认密码内容
            self.driver.send_keys(password_phone)  # 输入一致的密码
            if self.exists(label='The two passwords you entered did not match') is False:
                output_data['password_pass'] = True

            self.click_exists(2, label="NEXT")  # 点击下一步next
            time.sleep(3)
            if self.exists(label='Finish Registering'):
                output_data['register_pass'] = True
                self.click_exists(label="NEXT")
        print(output_data)
        return output_data

    # 邮箱注册
    def email_register(self, register_email, password_email):
        output_data = {'email_suffix': False, 'email_exits': False, 'message_send': False, 'message_fault_valid': False,
                       'message_right_valid': False, 'password_short_valid': False, 'password_long_valid': False,
                       'password_same_valid': False, 'password_pass': False, 'register_pass': False}
        self.login.signin_entry()
        self.login.history_login(isRemove=True)
        self.click_offset(offset=(0.8, 0.5), label=tv_create_account)  # 点击注册 No account
        self.click_exists(2, label=tv_email)  # 点击邮箱注册
        self.click_exists(2, className="TextField")  # 点击邮箱输入框
        suffix = "test001@"
        self.driver.send_keys(suffix)  # 输入未完整邮箱校验后缀
        time.sleep(3)
        if self.exists(className="StaticText", label=suffix + "gmail.com") \
                and self.exists(className="StaticText", label=suffix + "hotmail.com") \
                and self.exists(className="StaticText", label=suffix + "yahoo.com"):
            print("邮箱后缀校验成功")
            output_data['email_suffix'] = True

        self.clear_text(className="TextField")  # 先清空内容
        email_exist = rc.cf.get('Account', 'login_name_email')
        self.driver.send_keys(email_exist)  # 输入存在的邮箱
        self.click_exists(2, label=btn_send_email_code_register)  # 点击发送验证码
        self.click_exists(2, label=dialog_confirm)  # 确认发送短信
        time.sleep(3)
        # 校验存在过的邮箱
        if self.exists(label='The account exists. Sign in'):
            print("账号存在校验显示成功")
            output_data['email_exits'] = True
        time.sleep(3)
        self.click_exists(2, className="TextField")  # 点击邮箱输入框
        self.click_exists(2, label="Clear text")
        self.driver.send_keys(register_email)  # 输入没有注册过的手机号
        self.click_exists(2, label=btn_send_email_code_register)  # 点击发送验证码
        self.click_exists(2, label=dialog_confirm)  # 确认发送验证码
        time.sleep(8)
        if self.exists(label='The verification code has been sent to your email.'):
            print("验证码发送成功")
            output_data['message_send'] = True
            self.xpath_click_exists(2, xpath=yan_zheng_ma)
            for shu in '0000':
                self.click(label=shu)  # 输入错误验证码
            time.sleep(3)
            if self.exists(label='This code you entered is incorrect. Please try again.'):
                print("错误验证码校验成功")
                output_data['message_fault_valid'] = True
                self.xpath_click_exists(2, xpath=yan_zheng_ma)  # 点击验证码输入框
                for i in range(4):
                    self.click(label='Delete')  # 删除错误验证码
            time.sleep(3)
            # 获取数据库验证码
            data = RegisterModel().get_email_code(register_email)
            yzm_right = data['code']
            for i in yzm_right:
                self.click(label=i)  # 输入正确验证码
            time.sleep(3)
            if self.exists(label="Set Password"):  # ios验证码正确后直接跳转到下一页了
                print("正确验证码校验成功")
                output_data['message_right_valid'] = True

            self.click(label='register see', index=1)
            self.click(className='TextField', index=1)  # 点击第一个密码输入框
            short_password = "12345"
            self.driver.send_keys(short_password)  # 输入特别短的密码

            self.click(label='register see', index=2)
            self.click(className='TextField', index=2)  # 点击确认密码输入框
            self.driver.send_keys(short_password)  # 输入特别短的密码
            self.click_exists(label='NEXT')
            time.sleep(3)
            if self.exists(label='The password can not be less than 6 characters!'):
                print("短密码校验成功")
                output_data['password_short_valid'] = True

            long_password = "12345678912345678910"
            self.clear_text(className='TextField', index=1)  # 清空第一个密码输入框内容
            self.driver.send_keys(long_password)  # 输入特别长的密码
            self.click_exists(label='NEXT')
            time.sleep(3)
            if self.info('text', label='The password can not be more than 18 letters!'):
                print("长密码校验成功")
                output_data['password_long_valid'] = True

            self.clear_text(className='TextField', index=1)  # 清空第一个密码输入框内容
            self.driver.send_keys(password_email)  # 输入格式正确的密码

            self.clear_text(className='TextField', index=2)  # 清空第二个密码输入框内容
            reverse_password = password_email[::-1]
            self.driver.send_keys(reverse_password)  # 输入不一致的密码
            self.click_exists(2, label='NEXT')  # 点击下一步next
            time.sleep(3)
            if self.exists(label='The two passwords you entered did not match'):
                print("密码不一致校验成功")
                output_data['password_same_valid'] = True

            self.clear_text(className='TextField', index=2)  # 清空确认密码内容
            self.driver.send_keys(password_email)  # 输入一致的密码
            if self.exists(label='The two passwords you entered did not match') is False:
                output_data['password_pass'] = True

            self.click_exists(2, label="NEXT")  # 点击下一步next
            time.sleep(3)
            if self.exists(label='Finish Registering'):
                output_data['register_pass'] = True
                self.click_exists(label="NEXT")
        print(output_data)
        return output_data


def run_case(device):
    d = Driver.init_ios_driver(device)
    registerPage = RegisterPage(d)
    registerPage.email_register('test2022@test.com', '123456')
    # RegisterModel().del_email_register('test2022@test.com')
    # registerPage.phone_register('7017202201', '123456')
    # RegisterModel().del_phone_register('7017202201')


if __name__ == '__main__':
    device_list = get_ios_devices_list()
    with multiprocessing.Pool(len(device_list)) as pool:
        pool.map(run_case, device_list)
