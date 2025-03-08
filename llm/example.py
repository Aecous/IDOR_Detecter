from idlelib.pyparse import trans

from mitmproxy import http
from openai import OpenAI

from llm.LLM import LLM
from utils.requestutil import get_raw_request, get_raw_response

llm = LLM()

def call_llm_api(source_flow: http.HTTPFlow,modify_flow: http.HTTPFlow) -> str:
    #源请求体和响应体
    source_reques = get_raw_request(source_flow, source_flow.request.pretty_host)
    source_response = get_raw_response(source_flow)
    #修改后的请求体和响应体
    modify_request = get_raw_request(modify_flow, modify_flow.request.pretty_host)
    modify_response = get_raw_response(modify_flow)



    return llm.check(source_reques,source_response,modify_request,modify_response)
