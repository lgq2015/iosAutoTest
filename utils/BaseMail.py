from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import smtplib
from email.mime.application import MIMEApplication
from utils.BaseReadConfig import ReadConfig
from utils.BaseInitPath import InitPath


class SentMail:
    def __init__(self, to_addr, subject):
        rc = ReadConfig()
        self.smtp_server = 'smtp.qiye.163.com'
        self.from_addr = rc.get_admin_account()
        self.my_psw = rc.get_admin_password()
        self.to_addr = to_addr
        self.subject = subject
        self.msg = MIMEMultipart()

    def _format_addr(self, string):
        name, addr = parseaddr(string)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def _html_content(self):
        self.content = '''
        <html><body><h1>你好:</h1>
        <h2>测试报告请参考附件，注意此报告为自动邮件，请不要回复。</h2>
        <p>allure 报告结果</p>
        </body></html>'''
        return self.content

    def add_header(self):
        self.msg['From'] = self._format_addr(f'管理员<{self.from_addr}>')
        self.msg['To'] = self._format_addr(f'收件人<{self.to_addr}>')
        self.msg['Subject'] = Header(self.subject, 'utf-8').encode()

    def add_img(self, img_path):
        '''
        :param img_path: 图片路径：path + name
        :return:
        '''
        with open(img_path, 'rb') as f:
            # 图片添加到附件
            mime = MIMEBase('image', 'image', filename=img_path)
            mime.add_header('Content-Disposition', 'attachment', filename=img_path)
            mime.set_payload(f.read())
            encoders.encode_base64(mime)
            self.msg.attach(mime)

    def add_attachment(self, file_path, attch_name):
        '''
        :param file_path:文件路径：path + name
        :param attch_name: 附件名称
        :return:None
        '''
        with open(file_path, 'rb') as f:
            # MIMEBase表示附件的对象
            mime = MIMEApplication(f.read())
            # filename是显示附件名字
            mime.add_header('Content-Disposition', 'attachment', filename=attch_name)
            # 作为附件添加到邮件
            self.msg.attach(mime)

    def add_html(self):
        self.msg.attach(MIMEText(self._html_content(), _subtype='html', _charset='utf-8'))

    def add_text(self, text):
        self.msg.attach(MIMEText(_text=text, _subtype='plain', _charset='utf-8'))

    def sent_mail(self):
        ret = True
        try:
            server = smtplib.SMTP(self.smtp_server, 25)
            server.set_debuglevel(1)
            server.login(self.from_addr, self.my_psw)
            server.sendmail(self.from_addr, self.to_addr, str(self.msg))
            server.quit()
            print('邮件发送')
        except smtplib.SMTPException as e:
            ret = False
            print(e)
        return ret


if __name__ == '__main__':
    mail = SentMail(to_addr='609223909@qq.com', subject='自动化测试报告')
    mail.add_header()
    mail.add_html()
    report_path = InitPath.get_report_path('22932a78f00d7ece-2020-07-03_22.17.10/report.zip')
    mail.add_attachment(file_path=report_path, attch_name='report.zip')
    mail.sent_mail()
