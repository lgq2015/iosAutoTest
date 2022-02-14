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
dialog_confirm = "OK"
register_mobile_area_tv = "ic_arrow"
tv_create_account = "No account？Register"
tv_phone = "Phone Number"
tv_email = "Email Address"
get_code = "GET CODE"
yan_zheng_ma = '//Window[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[3]/Other[2]'
shouji_yan_zheng_ma = '//Window[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[3]/Other[3]'
accout_exist = 'The account exists. Sign in'
phone_send_success_tip = 'The verification code has been sent to your phone.'
email_send_success_tip = 'The verification code has been sent to your email.'
error_yzm_tip = 'This code you entered is incorrect. Please try again.'


class RegisterPage(PublicWdaIOSPage):

    def __init__(self, driver):
        super().__init__(driver)
        self.login = LoginPage(driver)

    # 手机注册
    def phone_register(self, register_phone, password_phone):
        output_data = {'phone_exits': False, 'message_send': False, 'message_fault_valid': False, 'tip_sign_in': False,
                       'message_right_valid': False, 'password_short_valid': False, 'password_long_valid': False,
                       'password_same_valid': False, 'password_pass': False, 'register_pass': False}
        self.login.signin_entry()
        self.login.history_login(isRemove=True)
        self.click_offset(offset=(0.8, 0.5), label=tv_create_account)  # # 点击注册
        self.click_exists(2, label=tv_phone)  # 点击手机号注册
        self.click_exists(2, name=register_mobile_area_tv)  # 切换国家
        self.click_exists(5, label="Nigeria")  # 切换Niger
        self.click_exists(2, className="TextField")  # 点击手机号输入框
        self.click_exists(2, label="Clear text")  # 先清空
        self.driver.send_keys(rc.cf.get('Account', 'login_name_phone'))  # 输入存在的手机号
        self.click_exists(2, label=get_code)  # 点击发送验证码
        self.click_exists(2, label=dialog_confirm)  # 确认发送短信
        time.sleep(3)
        # 校验存在过的手机号
        if self.exists(label=accout_exist):
            print("账号存在校验显示成功")
            output_data['phone_exits'] = True
            self.click_offset(offset=(0.5, 0.5), label=accout_exist)  # 点击提示语里的Sign in
            time.sleep(3)
            if self.exists(label='Sign in by email'):
                print("点击提示语里的Sign in进入登录页成功")
                output_data['tip_sign_in'] = True
                self.click(label='navi back')
        time.sleep(3)
        self.clear_text(className="TextField")  # 先清空内容
        self.driver.send_keys(register_phone)  # 输入没有注册过的手机号
        self.click_exists(2, label=get_code)  # 点击发送验证码
        self.click_exists(2, label=dialog_confirm)  # 确认发送短信
        time.sleep(3)
        if self.wait_exists(15, label=phone_send_success_tip):
            print("验证码发送成功")
            output_data['message_send'] = True
            # self.xpath_click_exists(5, xpath=shouji_yan_zheng_ma)
            self.click_outer_offset(offset=(30, -30), label=phone_send_success_tip)
            for shu in '0000':
                self.click(label=shu)  # 输入错误验证码
            time.sleep(3)
            if self.exists(label=error_yzm_tip):
                print("错误验证码校验成功")
                output_data['message_fault_valid'] = True
                # self.xpath_click_exists(5, xpath=shouji_yan_zheng_ma)  # 点击验证码输入框
                self.click_outer_offset(offset=(30, -30), label=error_yzm_tip)
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
                       'tip_sign_in': False, 'password_same_valid': False, 'password_pass': False,
                       'register_pass': False}
        self.login.signin_entry()
        self.login.history_login(isRemove=True)
        self.click_offset(offset=(0.8, 0.5), label=tv_create_account)  # 点击注册 No account
        self.click_exists(2, label=tv_email)  # 点击邮箱注册
        self.click_exists(2, className="TextField")  # 点击邮箱输入框
        self.click_exists(2, label="Clear text")  # 先清空
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
        self.click_exists(2, label=get_code)  # 点击发送验证码
        self.click_exists(2, label=dialog_confirm)  # 确认发送短信
        time.sleep(3)
        # 校验存在过的邮箱
        if self.exists(label=accout_exist):
            print("账号存在校验显示成功")
            output_data['email_exits'] = True
            self.click_offset(offset=(0.4, 0.5), label=accout_exist)  # 点击提示语里的Sign in
            time.sleep(3)
            if self.exists(label='Sign in by phone'):
                print("点击提示语里的Sign in进入登录页成功")
                output_data['tip_sign_in'] = True
                self.click(label='navi back')
        time.sleep(3)
        self.click_exists(2, className="TextField")  # 点击邮箱输入框
        self.click_exists(2, label="Clear text")
        self.driver.send_keys(register_email)  # 输入没有注册过的手机号
        self.click_exists(2, label=get_code)  # 点击发送验证码
        self.click_exists(2, label=dialog_confirm)  # 确认发送验证码
        time.sleep(3)
        if self.wait_exists(15, label=email_send_success_tip):
            print("验证码发送成功")
            output_data['message_send'] = True
            # self.xpath_click_exists(2, xpath=yan_zheng_ma)
            self.click_outer_offset(offset=(30, -30), label=email_send_success_tip)
            for shu in '0000':
                self.click(label=shu)  # 输入错误验证码
            time.sleep(3)
            if self.exists(label=error_yzm_tip):
                print("错误验证码校验成功")
                output_data['message_fault_valid'] = True
                # self.xpath_click_exists(2, xpath=yan_zheng_ma)  # 点击验证码输入框
                self.click_outer_offset(offset=(30, -30), label=error_yzm_tip)
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
    # registerPage.email_register('test2022@test.com', '123456')
    # RegisterModel().del_email_register('test2022@test.com')
    registerPage.phone_register('7017202201', '123456')
    RegisterModel().del_phone_register('7017202201')


if __name__ == '__main__':
    device_list = get_ios_devices_list()
    with multiprocessing.Pool(len(device_list)) as pool:
        pool.map(run_case, device_list)
