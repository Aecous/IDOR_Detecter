import yaml
from utils.singleton import Singleton
from utils.pathutil import path_join

#单例模式，确保config类只有一个实例存在，避免了多个配置实例之间可能存在的数据不一致性
@Singleton
class Config(object):
    #初始化config
    def __init__(self) -> None:
        self.config = None

    def parse_config(self) -> None:
        with open("config/config.yml", 'r', encoding='utf-8') as f:
            #使用safe load避免yaml反序列化漏洞攻击
            config = yaml.safe_load(f)
        try:
            #读取相关配置 host port cookie matchreplace
            for host in config['host']:
                self.config['host'].append(host)
            for port in config['port']:
                self.config['port'].append(port)
            self.config['cookie'] = config['cookie']
            for mrs in config['matchreplace']:
                self.config['mrs'].append(mrs)
        except Exception as e:
            print("Error: 配置解析出错")
            exit(0)

    #获取config
    def get_config(self) -> dict:
        if self.config is None:
            self.config = {
                'host': [],
                'port': [],
                'cookie': '',
                'mrs': []
            }
            self.parse_config()
        return self.config

    #对config进行检查
    def check_config(self) -> bool:
        if ('host' not in self.config) or ('cookie' not in self.config) or ('mrs' not in self.config):
            print("Error: 配置出错，请检查")
            return False
        if type(self.config['host']) != list or type(self.config['mrs']) != list or type(self.config['cookie']) != str:
            print("Error: 配置出错，请检查")
            return False
        return True



