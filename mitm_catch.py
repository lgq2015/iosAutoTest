import mitmproxy
from mitmproxy import http, tcp
from mitmproxy.coretypes.multidict import MultiDictView
#  命令行执行脚本时,提示导入的包找不到的问题 常用的只有一种：经交互时用的脚本放在根目录下
from utils.BaseInitPath import InitPath
import typing
from mitmproxy import ctx

getUrls = ["http://10.0.243.111:8080/i?logtype=event&events=",
           "https://event.startimestv.com"
           ]
find_action = {
    "video_play": {
        "desc": "视频开始播放时发送",
        "expect": {
            "vtype": "live",  # 直播频道
            "chid": "904461541",  # 频道ID
            "kids": "1",  # 儿童模式上报
        }
    },
    "video_pause": {
        "desc": "视频暂停时报送",
        "expect": {
            "vtype": "live",  # 直播频道
            "chid": "904461541",  # 频道ID
            "kids": "1",  # 儿童模式上报
        }
    }
}


class Catch:
    def __init__(self):
        self.num = 0

    def load(self, loader):
        loader.add_option(
            name="action",
            typespec=typing.Optional[str],
            default=None,
            help="Add a filter action",
        )

    def any_match(self, list, str: str):
        lower_str = str.lower()
        for i in list:
            if i in lower_str:
                return True
        return False

    # def tcp_start(self, flow: tcp.TCPFlow):
    #     req = flow.request
    #     url = req.pretty_url
    #     print(url)
    #
    # def tcp_message(self, flow: tcp.TCPFlow):
    #     req = flow.request
    #     url = req.pretty_url
    #     print(url)
    def tcp_error(self, flow: tcp.TCPFlow):
        req = flow.request
        url = req.pretty_url
        print("tcp error:"+url)


    def request(self, flow: http.HTTPFlow):
        req = flow.request
        url = req.pretty_url
        # print(url)
        if req.method == 'GET' and self.any_match(getUrls, url):
            self.dispatch_api(req)

    def error(self, flow: http.HTTPFlow):
        req = flow.request
        url = req.pretty_url
        print("http error:"+url)

    def dispatch_api(self, request):
        queryValue: MultiDictView = request.query
        logtype = queryValue.get("logtype")
        if logtype == "event":
            if ctx.options.action is not None:
                findAction = ctx.options.action
                self.event_single_handle(queryValue, findAction, find_action[findAction]['expect'])
            else:
                self.event_all_handle(queryValue)
        elif logtype == "pv":
            print("pv")
        else:
            print("no logtype")

    # 寻找单个埋点测试
    def event_single_handle(self, queryValue, findAction="video_play", expectColumn=None):
        events = queryValue.get("events")
        if isinstance(events, str) and len(events) > 0:
            urlMsg = eval(events)[0]["msg"]  # eval字符串转列表
            urlAction = urlMsg["action"]
            # print(urlMsg)
            if findAction == urlAction:
                desc = find_action[findAction]['desc']
                self.writeLog('%s --%s --埋点找到' % (findAction, desc))
                # 找到埋点后的处理
                if expectColumn is not None:
                    self.find_result(urlMsg, expectColumn)
            else:
                pass
                # self.writeLog('%s --埋点没有找到，现在的埋点是 %s' % (findAction, urlAction))

    # 寻找所有埋点测试
    def event_all_handle(self, queryValue):
        events = queryValue.get("events")
        if isinstance(events, str) and len(events) > 0:
            urlMsg = eval(events)[0]["msg"]  # eval字符串转列表
            urlAction = urlMsg["action"]
            actions = list(find_action.keys())  # 转换为列表
            if self.any_match(actions, urlAction):
                desc = find_action.get(urlAction)['desc']
                expectColumn = find_action[urlAction]['expect']
                # 找到埋点后的处理
                self.writeLog('%s --%s --埋点找到' % (urlAction, desc))
                if expectColumn is not None:
                    self.find_result(urlMsg, expectColumn)
            else:
                self.writeLog('%s --不是寻找埋点' % urlAction)

    # 找到埋点后的处理
    def find_result(self, urlMsg, expectColumn):
        columns = list(expectColumn.keys())  # 转换为列表
        for column in columns:
            if (column in urlMsg) and expectColumn[column] == urlMsg[column]:
                content = '字段%s --埋点符合，期望是%s ,实际是 %s' % (column, expectColumn[column], urlMsg.get(column, None))
            else:
                content = '字段%s --埋点不符合，期望是%s ,实际是 %s' % (column, expectColumn[column], urlMsg.get(column, None))
            self.writeLog(content)

    def writeLog(self, content):
        print(content)
        with open(InitPath.get_log_path("mitmproxy.log"), 'a+') as fp:
            fp.write('\n' + content)


addons = [
    Catch()
]
