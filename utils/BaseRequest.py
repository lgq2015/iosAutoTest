import json
import requests

from utils.BaseLog import Log

logger = Log(filename='request.log')
TIMEOUT = 10


class BaseRequest:
    def __init__(self, base_url=None):
        self.session = requests.session()
        self.base_url = base_url

    def get_req(self, url, payload=None, **kwargs):
        res = self.session.get(url, params=payload, **kwargs)
        return res

    def post_req(self, url, payload=None, **kwargs):
        res = self.session.post(url, data=payload, **kwargs)
        # res = requests.post(url, **kwargs)
        return res

    def delete_req(self, url, **kwargs):
        res = self.session.delete(url, **kwargs)
        return res

    def main_req(self, method, url, payload=None, **kwargs):
        url = self.base_url + url if self.base_url else url
        kwargs['timeout'] = kwargs.get('timeout', TIMEOUT)
        # kwargs.get('params') 、kwargs.get('json')
        logger.i(f"请求数据: \n method:{method} url:{url} \n payload:{payload} type:{type(payload)} \n kwargs:{kwargs}")

        if method.lower() == 'get':
            res = self.get_req(url, payload, **kwargs)
        elif method.lower() == "post":
            res = self.post_req(url, payload, **kwargs)
        elif method.lower() == "delete":
            res = self.delete_req(url, **kwargs)
        else:
            res = "你的请求方式暂未开放，请耐心等待"
        logger.i(f"响应数据: {res.text}")
        try:
            return res.json()  # {'name': 'wwy', 'sex': '男'}
            # return json.loads(res.text)
            # return res.text  # {"name":"wwy","sex":"\u7537"}
        except json.JSONDecodeError as e:
            return None


if __name__ == '__main__':
    data = ['http', 'ssh', 'ftp']  # 列表 有序key0\key1\key2
    data = ('http', 'ssh', 'ftp')  # 元组 有序key0\key1\key2 元素不能修改
    data = {            # 字典 无序 key：value
        'name': 'tom',
        'age': 18,
        'height': 1.80,
        'weight': 75.5
    }
    data = {'apple', 'orange', 'apple', 'pear', 'orange', 'banana'}  # 集合 无序 不重复元素序列
    print('----------------------------------------------------------------------------------')
    payload = {'title': 'title_get', 'content': 'content_get'}

    req = BaseRequest()
    print('get---------------')
    print(req.main_req('get', 'http://localhost/test.php', payload=payload))

    post_url = 'http://localhost/test.php'
    header = {
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        # "Content-Type": "application/json; charset=utf-8",
    }
    print('post---------------')
    print(req.main_req('post', post_url, payload=payload))
