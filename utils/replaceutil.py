import base64
import re
from base64 import decode
from sys import prefix
from urllib.parse import unquote, quote

base64_pattern = r'(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?'
hex_pattern = r'\b(?:0[xX])?[0-9a-fA-F]+\b'


def replace_base64(pattern, replace, origin) -> str:
    try:
        urlencode = False
        ##判断base64有无urlencode
        if "%" in origin:
            urlencode = True
            origin = unquote(origin)

        # 使用正则表达式查找所有匹配的Base64编码字符串
        ptn = re.compile(pattern)

        base64_matches = re.findall(base64_pattern, origin)
        # 如果存在Base64编码字符串，则尝试解码
        for match in base64_matches:
            try:
                decoded_data = base64.b64decode(match).decode('utf-8')
                # 查找解密后的是否存在匹配字符串
                for m in re.findall(ptn, decoded_data):
                    # 在解密后的字符串中进行替换
                    decoded_data = decoded_data.replace(m, replace)
                    # 重新加密，替换加密字符串
                    origin = origin.replace(match, base64.b64encode(decoded_data.encode('utf-8')).decode('utf-8'))
            except Exception as e:
                continue
        if urlencode:
            return quote(origin)
        return origin
    except Exception as e:
        return origin


def replace_hex(pattern, replace, origin) -> str:
    prefix = 0
    # 使用正则表达式查找所有匹配的16进制字符串
    ptn = re.compile(pattern)
    hex_matches = re.findall(hex_pattern,origin)
    # 解密16进制字符串为ASCII字符串
    decoded_data = ""
    for match in hex_matches:
        # 去除可能存在的前缀"0x"或"0X"
        if match.startswith("0x"):
            prefix = 1
            match = match[2:]
        elif match.startswith("0X"):
            prefix = 2
            match = match[2:]
        try:
            ascii_text = bytes.fromhex(match).decode('utf-8')
            decoded_data += ascii_text
        except ValueError:
            decoded_data += f"[Invalid Hex: {match}]"
        # 查找解密后是否存在需要替换的字符串
        for m in re.findall(ptn, decoded_data):
            decoded_data = decoded_data.replace(m, replace)
            if prefix == 1:
                replace_str = "0x" + decoded_data.encode('utf-8').hex()
            elif prefix == 2:
                replace_str = "0X" + decoded_data.encode('utf-8').hex()
            origin = origin.replace(match, decoded_data.encode('utf-8').hex())
    return origin


def replace_urlencode(pattern, replace, origin) -> str:
    try:
        decoded_data = origin
        ptn = re.compile(pattern)
        if "%" in origin:
            decoded_data = unquote(origin)
        for m in re.findall(ptn, decoded_data):
            # 在解密后的字符串中进行替换
            # decoded_data = decoded_data.replace(m, replace)
            # 重新加密，替换加密字符串
            origin = quote(decoded_data.replace(m,replace))
        return origin
    except Exception as e:
        return origin

def decode_hex(origin) -> str:
    try:
        ascii_text = bytes.fromhex(match).decode('utf-8')
        decoded_data += ascii_text
    except ValueError:
        decoded_data += f"[Invalid Hex: {match}]"

##测试
# if __name__ == '__main__':
#     patter = "Aecous"
#     replace = "123456"
#     origin = "--++--Aecous--++--"


    # origin = base64.b64encode(origin.encode('utf-8')).decode('utf-8')
    # test = replace_base64(patter, replace, origin)
    # print(test)
    # print(base64.b64decode(test).decode('utf-8'))

    # origin = quote(origin)
    # test = replace_urlencode(patter, replace, origin)
    # print(test)
    # print(unquote(test))

    # decode = ""
    # origin = origin.encode('utf-8').hex()
    # test = replace_hex(patter, replace, origin)
    # print(test)
    #
    # ascii_text = bytes.fromhex(test).decode('utf-8')
    # decode += ascii_text
    # print(decode)