import multiprocessing

from test.ios_test.common.PublicWdaIOSPage import PublicWdaIOSPage
from test.ios_test.starWdaIOS.pages.HomePage import HomePage
from utils.BaseDevicesInfo import get_ios_devices_list
from utils.BaseDriver import Driver
from utils.BaseReadConfig import ReadConfig
import time

# 页面元素 ---------------------------------
tv_login = "SIGN IN"
facebook_login = "SIGN IN WITH FACEBOOK"
dialog_confirm = "CONFIRM"
tv_remove_account = "Remove this account"
bn_login = "SIGN IN WITH STARTIMES ON ACCOUNT"
tv_area_name = "ic_arrow"
iv_area_name = "Nigeria"
tv_next = "NEXT"
tv_sign_in = "SIGN IN"
textinput_error = "The password is incorrect"
password_toggle = "register see"
sign_in_phone_text = "Sign in by phone"
sign_in_email_text = "Sign in by email"
history_account = 'SIGN IN WITH "'
account_exists = 'The account doesn.?t exist.  Register'


class LoginPage(PublicWdaIOSPage):

    def __init__(self, driver):
        super().__init__(driver)
        self.home = HomePage(driver)

    # 退出登录方法
    def logout(self):
        self.window_close()
        self.click_bottom_menu('me')
        self.scroll(direction='down', distance=1.5, className='CollectionView')
        if self.wait_exists(5, label="Settings"):
            self.click_exists(label="Settings")
        time.sleep(2)
        self.scroll(direction='down', distance=1.5, className='CollectionView')
        if self.wait_exists(5, label='SIGN OUT'):
            self.click(label='SIGN OUT')
            self.click(className="Button", label="OK")
            return True
        else:
            return False

    # 是否存在历史记录账号，是移除还是登录
    def history_login(self, isRemove=False):
        if isRemove is True:
            self.click_exists(2, label=tv_remove_account)
            self.click_exists(2, label=dialog_confirm)
        else:
            self.click_exists(2, labelContains=history_account)
            time.sleep(3)
        return True

    # 进入登录页面
    def signin_entry(self):
        self.window_close()
        self.click_bottom_menu('me')
        if self.exists(label=tv_login) is False:
            self.logout()
            # if self.wait_exists(timeout=10, name="topBar_logo"):
            if self.wait_exists(timeout=10, label="Me"):
                self.click_bottom_menu('me')
        self.click_gone(maxretry=3, label=tv_login)  # click一次点击有时候存在点不上的情况
        if self.exists(label="Terms of Service and Privacy Policy.") is True:
            return True
        else:
            return False

    def __login_handle(self, name, password):
        self.click(className="TextField")
        self.click_exists(2, label="Clear text")
        self.driver.send_keys(name)

        if self.info('enabled', label=tv_next) is True:
            self.click(label=tv_next)

        time.sleep(3)
        if self.exists(label=password_toggle) is True:
            self.click(label=password_toggle)
            self.click(className="TextField")
            self.driver.send_keys('1234567')  # 输入错误的密码

        if self.info('enabled', label=tv_sign_in) is True:
            self.click(label=tv_sign_in)
            time.sleep(3)
            if self.exists(label=textinput_error):
                self.clear_text(className="TextField")
                self.set_text(text=password, className="TextField")
                self.click(label=tv_sign_in)
        time.sleep(3)
        self.window_close()
        self.click_bottom_menu('me')

    # 手机账号不存在登录
    def signin_phone_not_exist_login(self, login_phone_not_exist='7017222222'):
        self.signin_entry()
        self.history_login(isRemove=True)
        # 点击sign in with startimes on account按钮
        self.click_exists(2, label=bn_login)
        self.click_exists(2, label=sign_in_phone_text)
        self.click_exists(2, name=tv_area_name)
        self.click_exists(5, label="Nigeria")

        output_data = {'phone_not_exits_tip': False, 'phone_not_exits_go_register': False}

        self.click(className="TextField")
        self.click_exists(2, label="Clear text")
        self.driver.send_keys(login_phone_not_exist)  # 输入不存在的手机账号
        if self.info('enabled', label=tv_next) is True:
            self.click(label=tv_next)
        time.sleep(3)
        if self.exists(nameMatches=account_exists):  # 里面有单引号 报错 \' 这么写也不行
            self.print('输入不存在的手机账号 校验成功')
            output_data['phone_not_exits_tip'] = True
            self.click_offset(offset=(0.7, 0.5), nameMatches=account_exists)  # 点击提示语注册Register
            time.sleep(3)
            if self.exists(label='Enter your Phone Number'):
                self.print('输入不存在的手机账号 点击提示语的Register跳转到手机注册页 校验成功')
                output_data['phone_not_exits_go_register'] = True
                self.click(label='navi back')
        print(output_data)
        return output_data

    # 手机登录
    def signin_phone_login(self, login_name_phone, password_phone):
        self.signin_entry()
        self.history_login(isRemove=True)
        # 点击sign in with startimes on account按钮
        self.click_exists(2, label=bn_login)
        self.click_exists(2, label=sign_in_phone_text)
        self.click_exists(2, name=tv_area_name)
        self.click_exists(5, label="Nigeria")
        self.__login_handle(login_name_phone, password_phone)
        if self.wait_exists(5, labelContains=login_name_phone):
            return True
        else:
            return False

    # 手机账号历史登录
    def signin_phone_history_login(self, login_name_phone):
        self.signin_entry()
        self.history_login(isRemove=False)
        self.window_close()
        self.click_bottom_menu('me')
        if self.wait_exists(5, textContains=login_name_phone):
            return True
        else:
            return False

    # 邮箱账号不存在登录
    def signin_email_not_exist_login(self, login_email_not_exist='test2222@test.com'):
        self.signin_entry()
        self.history_login(isRemove=True)
        self.click_exists(2, label=bn_login)
        self.click_exists(2, label=sign_in_email_text)

        output_data = {'email_not_exits_tip': False, 'email_not_exits_go_register': False}
        self.click(className="TextField")
        self.click_exists(2, label="Clear text")
        self.driver.send_keys(login_email_not_exist)  # 输入不存在的手机账号
        if self.info('enabled', label=tv_next) is True:
            self.click(label=tv_next)
        time.sleep(3)
        if self.exists(nameMatches=account_exists):
            self.print('输入不存在的邮箱账号 校验成功')
            output_data['email_not_exits_tip'] = True
            self.click_offset(offset=(0.5, 0.5), nameMatches=account_exists)  # 点击提示语注册Register
            time.sleep(3)
            if self.exists(label='Enter your email address'):
                self.print('输入不存在的邮箱账号 点击提示语的Register跳转到邮箱注册页 校验成功')
                output_data['email_not_exits_go_register'] = True
                self.click(label='navi back')
        print(output_data)
        return output_data

    # 邮箱登录
    def signin_email_login(self, login_name_email, password_email):
        self.signin_entry()
        self.history_login(isRemove=True)
        # 点击sign in with startimes on account按钮
        self.click_exists(2, label=bn_login)
        self.click_exists(2, label=sign_in_email_text)

        self.__login_handle(login_name_email, password_email)
        if self.wait_exists(5, labelContains=login_name_email):
            return True
        else:
            return False

    # 邮箱账号历史登录
    def signin_email_history_login(self, login_name_email):
        self.signin_entry()
        self.history_login(isRemove=False)
        self.window_close()
        self.click_bottom_menu('me')
        if self.wait_exists(5, textContains=login_name_email):
            return True
        else:
            return False


def run_case(device):
    d = Driver.init_ios_driver(device)
    loginPage = LoginPage(d)

    # loginPage.signin_phone_not_exist_login()
    # loginPage.signin_phone_login('7017888888', '123456')
    # loginPage.signin_phone_history_login('7017888888')
    # loginPage.signin_email_not_exist_login()
    # loginPage.signin_email_login('609223909@qq.com', '123456')
    # loginPage.signin_email_history_login('609223909@qq.com')

    # loginPage.logout()
    # loginPage.signin_entry()


if __name__ == '__main__':
    rc = ReadConfig()
    device_list = get_ios_devices_list()
    with multiprocessing.Pool(len(device_list)) as pool:
        pool.map(run_case, device_list)
