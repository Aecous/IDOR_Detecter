import sys
import os
import shutil
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.pathutil import path_join
from utils.requestutil import get_raw_request, resp_htmlencode, get_raw_response


class Output():
    def __init__(self, api, src_flow, mod_flow, src_resp, mod_resp, pretty_host,llmcheck) -> None:
        self.api = api
        self.src_flow = src_flow
        self.mod_flow = mod_flow
        self.src_resp = src_resp
        self.mod_resp = mod_resp
        self.pretty_host = pretty_host
        self.llmcheck = llmcheck
        self.__init_output_file()

    def __init_output_file(self) -> None:
        if not os.path.exists(path_join('report/report.md')):
            shutil.copyfile(path_join('report/report.tpl'), path_join('report/report.md'))

    def output(self) -> None:
        markdown = f"""## {self.src_flow.request.path}
### 原始请求
```
{get_raw_request(self.src_flow,self.pretty_host)}
```
### 原始响应包
```
{self.src_resp}
```
### 重放请求
```
{get_raw_request(self.mod_flow,self.pretty_host)}
```
### 重放响应包
```
{self.mod_resp}
```
### LLM分析
```
{self.llmcheck}
```


"""

        with open(path_join('report/report.md'), 'r') as f:
            content = f.read()
        with open(path_join('report/report.md'), 'w') as f:
            f.write(content.replace('********', f'{markdown}********').encode('utf-8').decode('utf-8'))

