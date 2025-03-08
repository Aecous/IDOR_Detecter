
import json
import Levenshtein
import mitmproxy.http as http


class Dor:
    def __init__(self, source_resp, modify_resp,source_flow : http.HTTPFlow) -> None:
        self.sr = source_resp
        self.mr = modify_resp
        self.sf = source_flow.copy()
        #新增info，后续将整理的info信息丢给LLM模型进行二次检测
        #长度、请求方法、提交参数、关键词、相似度
        # self.info = {
        #     "source_resp_length": len(source_resp),
        #     "modify_resp_length": len(modify_resp),
        #     "source_resp_body": source_resp,
        #     "modify_resp_body": modify_resp,
        #     "request_method": source_resp.method,
        #     "query": source_resp.query,
        #     "key_words": [],
        #     "similarity": self.__similarity(source_resp, modify_resp),
        # }
        #判断响应是否是json，是json则处理后再进行关键词提取
        # if self.__is_json(source_resp):
        #     l = self.__traverse_json(json.loads(self.mr))
        #     self.__key_words(" ".join(l))
        # else:
        #     #响应不是json，直接进行关键词提取
        #     self.__key_words(modify_resp)

    def __is_json(self, resp) -> bool:
        try:
            json.loads(resp)
            return True
        except Exception:
            return False

    def __traverse_json(self, json_obj, l=None) -> list:
        # 遍历json每一个元素
        if l is None:
            l = []
        for key, value in json_obj.items():
            if isinstance(value, dict):
                self.__traverse_json(value, l)
            elif type(value) == str:
                l.append(value)
        return list(set(l))

    def __public_api_check(self) -> bool:
        #非空检测
        if not self.sf:
            return False

        #判断公共接口
        if self.sf.request.method != 'GET':
            return False
        # 判断是否有参数
        if not self.sf.request.query:
            return True

        #清空参数并重放
        self.sf.request.query = []
        from core.replay import Replay
        no_query_paramater_resp = Replay.replay(self.sf)

        # 如果重放后相似，说明是公共接口
        return (
                self.__similarity(self.sr, no_query_paramater_resp) > 0.87
                and self.__similarity(self.mr, no_query_paramater_resp) > 0.87
                and self.__similarity(self.sr, self.mr) > 0.87
        )

    def detect_vuln(self) -> bool:

        #公共接口检查
        if self.__public_api_check():
            return False

        # 长度卡点，当长度大于100时，进行相似度检测
        if len(self.sr) >= 100 and len(self.mr) >= 100:
            #相似度检测
            return self.__similarity(self.sr, self.mr) > 0.87
        # 长度过短，进行关键字检查，json则连接成字符串再做判断
        if self.__is_json(self.mr):
            l = self.__traverse_json(json.loads(self.mr))
            if self.__key_words_check(" ".join(l)):
                return True
        elif self.__key_words_check(self.mr):
            return True

    def __key_words_check(self, resp) -> bool:
        keywords = ['success', 'ok', 'true', '成功', '完成', '查询成功', 'yes', '已修改', '已存在', '已添加', 'exists',
                    'already','200']
        keywords_copy = keywords[:]  # 复制关键词列表
        for word in keywords_copy:
            if word.isalpha():  # 仅处理完全由字母组成的单词
                keywords.extend((word.capitalize(), word.upper()))  # 添加英文单词的首字母大写形式和全部大写形式
        return any(keyword in resp for keyword in keywords)

    def __similarity(self, str1, str2) -> float:
        # sourcery skip: inline-immediately-returned-variable
        distance = Levenshtein.distance(str1, str2)
        max_length = max(len(str1), len(str2))
        similarity = (max_length - distance) / max_length
        return similarity

