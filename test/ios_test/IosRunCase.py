import multiprocessing
import pytest
import time
import subprocess
from utils.BaseDevicesInfo import get_ios_devices_list
from utils.BaseInitPath import InitPath
from utils.BaseReadConfig import ReadConfig
from utils.BaseZip import MyZip
from utils.BaseMail import SentMail
from utils.BaseGlobalVar import GlobalVar


class RunCase:
    # 初始化
    def __init__(self):
        self.rc = ReadConfig()
        self.init_path = InitPath()

    # 启动多进程
    def run(self, device_list):
        with multiprocessing.Pool(len(device_list)) as pool:
            pool.map(self.run_pytest, device_list)

    # 打开浏览器报告
    def _browser(self, report_path):
        print("====================_browser 打开浏览器===================")
        html_path = report_path + '/html'
        # Popen 不阻塞 不需要返回结果才接着运行下面代码
        subprocess.Popen("allure open {}".format(html_path), shell=True)

    # 压缩测试报告
    def _zip(self, report_path):
        print("====================_zip 压缩测试报告===================")
        html_path = report_path + '/html'
        myzip = MyZip()
        output_name = 'report.zip'
        zip_path = myzip.zip_file_path(input_path=html_path, output_path=report_path, output_name=output_name)
        return zip_path

    # 发送邮件
    def _sentMail(self, file_path, model):
        print("====================_sentMail 发送邮件===================")
        mail = SentMail(to_addr=self.rc.get_to_email(),
                        subject=self.rc.get_email_subject().format(model))
        mail.add_header()
        mail.add_html()
        attachment_name = model + '.zip'
        mail.add_attachment(file_path=file_path, attch_name=attachment_name)
        mail.sent_mail()

    # 运行
    def run_pytest(self, device):
        GlobalVar.set_value('device', device)

        # 初始化报告，日志 phone['serial']==device
        # phone = get_device_info(device)
        now = time.strftime('%Y-%m-%d_%H.%M.%S', time.localtime(time.time()))
        report_path = self.init_path.get_report_path(report_path=device + '-' + now)

        # 执行测试并生成测试报告
        print("====================start running test====================")
        print(f"sent 设备序列号serial ：{device}")
        print(f"report_path ： {report_path}")

        try:
            # print(self.rc.get_android_test_suite())
            pytest.main(["-v", "-m", f"{self.rc.get_mark('IosTest')}", f"{self.rc.get_ios_test_suite()}",
                         f"--device={device}", "--alluredir", f"{report_path}/xml"])
            time.sleep(1)
            # call阻塞 需要等待子进程执行结束 才接着运行self._zip
            subprocess.call(f"allure generate {report_path}/xml -o {report_path}/html", shell=True, close_fds=True)

            # 打开浏览器
            self._browser(report_path)

            # 压缩测试报告
            # zip_path = self._zip(report_path)
            # 发送邮件
            # self._sentMail(zip_path, phone['model'])

        except Exception as e:
            print(f"error occur {e}")


if __name__ == '__main__':
    case = RunCase()
    case.run(get_ios_devices_list())
