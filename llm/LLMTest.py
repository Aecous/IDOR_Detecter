 

import sys,os
import LLM
def log(*args):
    print('[Info]',*args)

class LLMTest:
    def __init__(self) -> None:
        self.test_example_dir = 'test_example'
        self.examples = self.import_modules_sys_path(self.test_example_dir)
        self.llm = LLM()

    def import_modules_sys_path(self,directory) ->list:
        sys.path.append(directory)  # 添加文件夹到 sys.path 中
        result = []
        for filename in os.listdir(directory):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = filename[:-3]  # 去掉 .py 后缀
                try:
                    module = __import__(module_name)
                    if hasattr(module,'source_request') and hasattr(module,'source_response') and hasattr(module,'modify_request') and hasattr(module,'modify_request'):
                        print(f"Successfully imported {module_name}")
                        result.append(module)
                    else:
                        print('Skip:',module)
                except Exception as e:
                    print(f"Failed to import {module_name}: {e}")
        return result
    
    def start(self):
        for example in self.examples:
            log('testing',example)
            self.llm.check(example.source_request,example.source_response,example.modify_request,example.modify_response)

