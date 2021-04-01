from mitmproxy import http
from mitmproxy import ctx
import urllib.parse

from mitmproxy.coretypes.multidict import MultiDictView

getUrls = ["http://10.0.243.111:8080/i?logtype=event&events="]
player_actions = {
    "video_play": "视频开始播放时发送",
    "video_pause": "视频暂停时报送",
    "video_resume": "视频暂停后重新播放时报送",
    "video_exit": "视频播放结束时发送",
    "share_tap": "点击分享按钮时报送",
    "video_replay": "点击视频重播按钮时发送"
}


class Counter:
    def __init__(self):
        self.num = 0

    def any_match(self, list, str: str):
        lower_str = str.lower()
        for i in list:
            if i in lower_str:
                return True
            return False

    def request(self, flow: http.HTTPFlow):
        request = flow.request
        url = request.pretty_url
        if request.method == 'GET' and self.any_match(getUrls, url):
            self.resolve(request)

    def resolve(self, request):
        queryValue: MultiDictView = request.query
        logtype = queryValue.get("logtype")
        if logtype == "event":
            events = queryValue.get("events")
            if isinstance(events, str) and len(events) > 0:
                action = eval(events)[0]["msg"]["action"]
                print(action)
                actions = player_actions.keys()
                msg = player_actions.values()
                if(self.any_match(actions, action)):
                    print(msg+"正常")
                else:
                    print(msg+"不正常")

        elif logtype == "pv":
            print("pv")
        else:
            print("no logtype")


addons = [
    Counter()
]
