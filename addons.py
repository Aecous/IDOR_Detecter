from urllib.parse import urlparse

import mitmproxy.http as http
from config.config import Config
from utils.requestutil import get_api
from utils.thread import my_thread
from core.replay import Replay
import re

class Listener:
    def __init__(self) -> None:
        #初始化config
        self.config = Config().get_config()
        #检测config是否合法
        if not Config().check_config():
            exit(0)

    #静态资源检测
    def __is_static(self, flow: http.HTTPFlow) -> bool:
        # 判断是否在请求静态资源
        path = urlparse(flow.request.url).path
        static_ext = ['.js', '.css', '.png', '.jpg', '.jpeg', '.gif', '.ico', '.svg', '.woff', '.woff2', '.ttf', '.eot',
                      '.map', '.ico', '.webp', 'htm', 'html']
        return any(path.endswith(ext) for ext in static_ext)

    def __is_vul_exists(self, flow: http.HTTPFlow) -> bool:
        # 判断漏洞是否已存在
        # return False  # for test only
        content = open('logs/vul.txt', 'r').read()
        return get_api(flow) in content

    def __check_port(self, flow: http.HTTPFlow) -> bool:
        port = flow.request.port
        for p in self.config['port']:
            if type(p) == type(0) and p == port:
                return True
            if type(p) == type('') and re.match(p, str(port)):
                return True
        return False


    def __check_host(self, flow: http.HTTPFlow) -> bool:
        host = flow.request.pretty_host
        for h in self.config['host']:
            try:
                pattern = re.compile(h)
                if re.match(pattern, host):
                    return True
            except Exception:
                if host == pattern:
                    return True
        return False

    def request(self, flow: http.HTTPFlow) -> None :
        # print(flow.request)
        pass



    def response(self, flow: http.HTTPFlow) -> None:
        #静态资源检测
        if self.__is_static(flow):
            return


        #判断请求中是否存在参数，如果不存在参数则直接返回响应不做漏洞检测
        if len(flow.request.query) < 1 and len(flow.request.content) < 1 :
            # print(flow.request.query)
            # print(flow.request.content)
            return

        if self.__check_host(flow) and self.__check_port(flow) and not self.__is_vul_exists(flow):
            my_thread(Replay, flow)
        else:
            a = 1 # 目的是让响应函数不为空


addons = [
    Listener()
]