import yaml
import json

class DataExchange:
    def __init__(self):
        pass

    # 从文件中读取yaml信息
    @staticmethod
    def yaml_load(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return data

    # 将yaml信息写进文件
    @staticmethod
    def yaml_dump(file_path, write_data):
        with open(file_path, 'w', encoding='utf-8') as fp:
            yaml.dump(write_data, fp)

    # json格式字符串转化为字典
    @staticmethod
    def json_loads(json_str):
        return json.loads(json_str)

    # 字典转化为字符串json格式
    @staticmethod
    def json_dumps(dict_data={}):
        return json.dumps(dict_data)
        # return json.dumps(dict_data, ensure_ascii=False, indent=4, sort_keys=True)

    # 从文件中读取json信息
    @staticmethod
    def json_load(file_path):
        with open(file_path, 'r', encoding='utf-8') as fp:
            data = json.load(fp)
        return data

    # 将json信息写进文件
    @staticmethod
    def json_dump(file_path, write_data):
        with open(file_path, 'w', encoding='utf-8') as fp:
            json.dump(write_data, fp)


if __name__ == '__main__':
    json_obj = DataExchange()
    # data = json_obj.json_load(file_path=InitPath.get_data_path('operate_json.json'))
    # print(data)
    # print(type(data))
    # print(data['login'])
    # print(data['login']['username'])
    print('-------------json_loads-----------------------')
    json_str = ' {"username": "wwy", "password": "121345"} '
    json_str = "{ 'title': 'title_get', 'content': 'content_get'}"
    json_str = ' { "title": "title_get", "content": "content_get"} '
    data = json_obj.json_loads(json_str)
    print(json_str)
    print(type(json_str))
    print(data)
    print(type(data))
    print(data['title'])
    # print('-------------json_dumps-----------------------')
    #
    # dict_data = {  # 字典 无序 key：value
    #     "username": "wwy",
    #     "password": "121345"
    # }
    # data = json_obj.json_dumps(dict_data)
    # print(data)
    # print(type(data))
    # print('-------------json_dump-----------------------')
    #
    # json_obj.json_dump(InitPath.get_data_path('test.json'), json_str)
    # json_obj.json_dump(InitPath.get_data_path('test.json'), dict_data)
    #
    # print('--------------yaml_load----------------------')
    #
    # yaml_obj = DataExchange()
    # data = yaml_obj.yaml_load(InitPath.get_data_path('api_data.yaml'))
    # print(data)
    # print(type(data))
    # print(data['valid_data_source_id'])
    # print('--------------yaml_load----------------------')
    #
    # dict_data = {
    #     "cookie1": {
    #         'domain': '.yiyao.cc',
    #         'expiry': 1521558688.480118,
    #         'httpOnly': False,
    #         'name': '_ui_',
    #         'path': '/',
    #         'secure': False,
    #         'value': 'HSX9fJjjCIImOJoPUkv/QA=='
    #     }
    # }
    # yaml_obj.yaml_dump(InitPath.get_data_path('test.yaml'), dict_data)
