from mitmproxy.tools.main import *
import warnings
warnings.filterwarnings("ignore")

if __name__ == '__main__':
    port = 10000
    print(f"[+] 启动HTTP代理http://127.0.0.1:{port}成功")
    mitmdump(args=['-p',f'{port}', '--mode','regular', '-s', 'addons.py', '-q'])


