import Crypto.Cipher.DES3
import base64

# 密钥
KEY = "PxFJTX5De/3Ta"

# 3DES根据16位对齐
BS = 16


# 补充字符,最少1个
def pad(s):
    length = len(s)
    add = BS - length % BS
    byte = chr(BS - length % BS)
    return (s + (add * byte)).encode()


# 去除补充字符
def unpad(s):
    length = len(s)
    byte = s[length - 1:]
    add = ord(byte)
    return s[:-add]


# 密钥补齐
def auto_fill(x):
    if len(x) > 24:
        raise Exception('密钥长度不能大于等于24位')
    else:
        while len(x) < 16:
            x += " "
    return x.encode()


# 加密
def encrypt(message, key=KEY):
    key = auto_fill(key)
    message = pad(message)
    cipher = Crypto.Cipher.DES3.new(key, Crypto.Cipher.DES3.MODE_ECB)
    crypto = base64.encodebytes(cipher.encrypt(message))
    return crypto


# 解密
def decrypt(crypto, key=KEY):
    key = auto_fill(key)
    cipher = Crypto.Cipher.DES3.new(key, Crypto.Cipher.DES3.MODE_ECB)
    message = cipher.decrypt(base64.decodebytes(crypto))
    message = unpad(message)
    return message
