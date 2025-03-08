from openai import OpenAI
import os


API_BASE = "https://api.bltcy.top/v1"
API_KEY = "???"
LLM_MODEL = "gpt-4o-mini"
# LLM_MODEL = "gpt-4"
# LLM_MODEL = "qwen-turbo"





def log(*args):
    print('[Info]',*args)

class LLM:
    def __init__(self,initialize:bool = True) -> None:
        self.api_base = API_BASE
        self.client = OpenAI(
            # 默认为os.environ.get("OPENAI_API_KEY")
            api_key=API_KEY, #0xA1pha的api key，刷完额度喊我
            base_url=self.api_base,
        )
        self.messages=[]
        self.vulnerable_example_dir = 'llm/vulnerable-example'
        self.secure_example_dir = 'llm/secure-example'
        self.start_prompt_dir = 'llm/start-prompt'
        self.end_prompt_dir = 'llm/end-prompt'
        if initialize:
            self.initialize()


    def wrap_msg(self,msg)->dict:
        return {
            "role": "user",
            "content": msg,
        }
    
    def feed_prompt(self,prompt_dir) -> None:
        files = os.listdir(prompt_dir)
        for filename in files:
            file_path = os.path.join(prompt_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                log('LLM reading prompt',file_path)
                self.messages.append(self.wrap_msg(content))

    def feed_vulnerable_example(self) ->None:
        self.feed_prompt(self.vulnerable_example_dir)
    def feed_secure_example(self) ->None:
        self.feed_prompt(self.secure_example_dir)
    def feed_start_prompt(self) ->None:
        self.feed_prompt(self.start_prompt_dir)
    def feed_end_prompt(self) ->None:
        self.feed_prompt(self.end_prompt_dir)

    def initialize(self) -> None:
        log('LLM start initializing')
        self.feed_start_prompt()
        self.feed_vulnerable_example()
        self.feed_secure_example()
        self.feed_end_prompt()
        log('LLM finished initializing')

    def chat(self,msg,printResult:bool = True) -> str:
        response = ''
        if printResult:
            log('=============== Start chatting ===============')
        chat_completion = self.client.chat.completions.create(
            messages=self.messages + [self.wrap_msg(msg)],
            model=LLM_MODEL,
        )
        response = chat_completion.choices[0].message.content
        if printResult:
            print(response)
            log('=============== End chatting ===============')
        return response

    def check(self,source_request,source_response,modify_request,modify_response)->str:
        log('Start checking API...')
        msg = '\nThis is new pair of request and response\n'
        msg += '\nrequest 1: \n'
        msg += source_request
        msg += '\nresponse 1: \n'
        msg += source_response
        msg += '\nrequest 2: \n'
        msg += modify_request
        msg += '\nresponse 2: \n'
        msg += modify_response
        # print(msg)
        result = self.chat(msg,False)
        log('Checking API finished','Detail:\n',result)

        return result
