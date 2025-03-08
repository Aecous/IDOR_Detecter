import base64
import contextlib
import json
import traceback
import re
import sys
import os
import llm.example
from utils.replaceutil import replace_base64, replace_hex, replace_urlencode

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mitmproxy.http as http
from mitmproxy import ctx
from mitmproxy import exceptions
from bs4 import BeautifulSoup
from config.config import Config
from utils.record import record
from utils.requestutil import get_api, get_raw_request, hack_request
from core.dor import Dor
from core.output import Output





class Replay:
    def __init__(self, source_flow: http.HTTPFlow) -> None:
        self.source_flow = source_flow
        # print(self.source_flow)
        # print(self.source_flow.request)
        self.pretty_host = self.source_flow.request.pretty_host
        #复制源请求并进行修改
        self.modify_flow = source_flow.copy()
        #获取api
        self.api = get_api(self.source_flow)

        # 过滤html接口
        source_resp = source_flow.response.text
        if self.__is_resp_html(source_resp):
            return

        # 判断接口是否为json格式
        #也不一定非得是json格式？只不过大部分都是
        # if not self.__is_resp_json(source_flow.response):
        #     return

        print(f"[*] 开始检测接口: {self.api}")

        #修改认证信息等，重访请求
        self.__modify_flow()
        modify_resp = self.replay(self.modify_flow)


        #进行idor漏洞检测
        if Dor(source_resp, modify_resp, source_flow).detect_vuln():
            print(f"[+] 发现漏洞 {self.api}")

            #使用LLM进行判断并给出原因
            llmcheck = llm.example.call_llm_api(source_flow, self.modify_flow)
            record(self.api, True)
            Output(self.api, self.source_flow, self.modify_flow, source_resp, modify_resp, self.pretty_host,llmcheck).output()
        else:
            record(self.api, False)

    def __is_resp_html(self, resp):
        # 检验是否为html响应
        return bool(BeautifulSoup(resp, "html.parser").find())

    def __is_resp_json(self, response: http.Response):
        # 检验是否为json响应
        if content_type := response.headers.get('Content-Type', ''):
            return content_type.startswith('application/') and 'json' in content_type
        try:
            json.loads(response.text)
            return True
        except Exception:
            return False

    def __parse_cookie(self, cookie: str) -> dict:
        cookie_dict = {}
        for c in cookie.split(';'):
            with contextlib.suppress(Exception):
                k, v = tuple(c.split('=', 1))
                cookie_dict[k] = v
        return cookie_dict

    def __modify_cookie(self, flow: http.HTTPFlow, new_cookie) -> None:
        # Modify the cookie here.
        flow.request.cookies.clear()

        for k, v in self.__parse_cookie(new_cookie).items():
            flow.request.cookies[k] = v

    def __replace(self, pattern, replace, origin):
        # 替换，若pattern为正则则正则替换，否则为字符串替换
        #正则表达式
        ptn = re.compile(pattern)

        #对参数进行base64解密后匹配替换
        origin = replace_base64(pattern, replace, origin)

        #对参数进行url解密后匹配替换
        origin = replace_hex(pattern, replace, origin)

        origin = replace_urlencode(pattern, replace, origin)



        try:
            #使用正则匹配进行替换
            return re.sub(ptn, replace, origin)
        except Exception:
            return origin.replace(pattern, replace)

    def __modify_flow(self) -> None:
        # Modify the flow here.
        config = Config().get_config()
        if config['cookie']:
            self.__modify_cookie(self.modify_flow, config['cookie'])
        self.__match_replace(self.modify_flow, config['mrs'])

    def __match_replace(self, flow: http.HTTPFlow, mrs: list) -> None:
        # Match and replace here.
        for mr in mrs:
            if mr['location'] == 'URL':
                flow.request.url = self.__replace(mr['pattern'], mr['replace'], flow.request.url)
            elif mr['location'] == 'PATH':
                flow.request.path = self.__replace(mr['pattern'], mr['replace'], flow.request.path)
            elif mr['location'] == 'BODY':
                flow.request.content = self.__replace(mr['pattern'], mr['replace'], flow.request.content.decode('utf-8')).encode('utf-8')
            elif mr['location'] == 'HEADER':
                header_name = mr['replace']['name']
                header_value = mr['replace']['value']
                if header_name in flow.request.headers:
                    # flow.request.headers[header_name] = self.__replace(mr['pattern'], header_value,flow.request.headers[header_name])
                    try:
                        # 使用正则匹配进行替换
                        ptn = re.compile(mr['pattern'])
                        flow.request.headers[header_name] = re.sub(ptn, header_value, flow.request.headers[header_name])
                    except Exception:
                        flow.request.headers[header_name] = flow.request.headers[header_name].replace(mr['pattern'], header_value)
                else:
                    flow.request.headers[header_name] = header_value
            elif mr['location'] == 'ALL':
                flow.request.path = self.__replace(mr['pattern'], mr['replace'], flow.request.path)
                flow.request.content = self.__replace(mr['pattern'], mr['replace'], flow.request.content.decode('utf-8')).encode('utf-8')


    @staticmethod
    def replay(*args) -> str:
        if len(args) == 1:
            flow = args[0]
            pretty_host = flow.request.pretty_host
        elif len(args) > 1:
            self = args[0]
            flow = args[1]
            pretty_host = self.pretty_host

        raw = get_raw_request(flow,pretty_host=pretty_host)
        try:
            return hack_request(raw, url=flow.request.url)
        except Exception as e:
            print(f"hack_request error: {e}")
            traceback.print_exc()
            return None
