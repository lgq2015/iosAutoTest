import os
import configparser
from utils.BaseInitPath import InitPath

config_path = InitPath.get_config_path('config.ini')


class ReadConfig:
    def __init__(self):
        self.cf = configparser.ConfigParser()
        self.cf.read(config_path, 'utf-8')

    def get_mark(self, platform='AndroidTest'):
        res = self.cf.get(platform, 'mark')
        return res

    def get_repeat(self):
        res = self.cf.get('AndroidTest', 'repeat')
        return res

    def get_to_email(self):
        res = self.cf.get('EMAIL', 'to_addr')
        return res

    def get_email_subject(self):
        res = self.cf.get('EMAIL', 'email_subject')
        return res

    def get_admin_account(self):
        res = self.cf.get('EMAIL', 'admin_addr')
        return res

    def get_admin_password(self):
        res = self.cf.get('EMAIL', 'admin_psw')
        return res

    def get_apk_path(self, whichApp='APP'):
        res = self.cf.get(whichApp, 'apk_path')
        return res

    def get_apk_url(self):
        res = self.cf.get('APP', 'apk_url')
        return res

    def get_apk_name(self, whichApp='APP'):
        res = self.cf.get(whichApp, 'apk_package_name')
        return res

    def get_app_start_activity(self):
        res = self.cf.get('APP', 'app_start_activity')
        return res

    def get_android_test_suite(self):
        res = InitPath.get_file_path(self.cf.get('AndroidTest', 'test_suite'))
        # res = self.cf.get('AndroidTest', 'test_suite')
        return res

    def get_ios_test_suite(self):
        res = InitPath.get_file_path(self.cf.get('IosTest', 'test_suite'))
        return res

    def get_api_test(self, key=None):
        config = {
            "test_suite": InitPath.get_file_path(self.cf.get('ApiTest', 'test_suite')),
            "api_names": self.cf.get('ApiTest', 'test_api_name').split('|')
        }
        if key is not None and config[key] is not None:
            return config[key]
        return config

    def get_database(self, db='DATABASE1'):
        config = {
            "host": self.cf.get(db, 'host'),
            "user": self.cf.get(db, 'user'),
            "password": self.cf.get(db, 'password'),
            "port": self.cf.getint(db, 'port'),
            "charset": self.cf.get(db, 'charset'),
            "database": self.cf.get(db, 'database')
        }
        # print(config)
        return config


if __name__ == '__main__':
    rc = ReadConfig()
    print(type(rc.get_to_email()))
    print(rc.get_apk_name('IOS_StarTimesOn'))
    print(rc.get_database())
