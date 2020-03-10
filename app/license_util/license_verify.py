import json
from .sysInfo import get_sysInfo
from app.rsa_util.rsa_tool import decrypt, get_publicKey, get_privateKey, sign_verify
import os
path = os.path.dirname(__file__)
licenseFile = os.path.join(path, 'license_data.json')


# 验证license
def license_verify():
    pubKey = get_publicKey()
    priKey = get_privateKey()

    # 设备指纹
    sysInfo = get_sysInfo()

    # 应当获取当地时间 # 还要写一个date工具
    curr_date = '2020-03-07'

    # 获取license数据
    with open(licenseFile, 'r') as f:
        result = json.loads(f.read())
    print('license:', '\n', result, '\n')

    license_content = result['content']
    license_signature = result['signature']
    license_sysInfo = license_content['sysInfo']
    license_valid_date = license_content['valid_date']

    # 数字签名验证
    verification = sign_verify(pubKey, license_signature, str(license_content))
    if not verification:
        ex = Exception('Signature Error.')
        raise ex

    # 密文验证
    crypto = license_sysInfo.encode('utf-8')
    try:
        decrypto = decrypt(priKey, crypto)
    except Exception:
        ex = Exception('Message Decryption Error.')
        raise ex
    print('decrypto:', '\n', decrypto, '\n')
    if decrypto != sysInfo:
        ex = Exception('Message Error.')
        raise ex

    # 有效期验证
    crypto = license_valid_date.encode('utf-8')
    try:
        valid_date = decrypt(priKey, crypto)
    except Exception:
        ex = Exception('Valid-Date Decryption Error.')
        raise ex
    print('valid_date:', '\n', valid_date, '\n')
    # if valid_date < curr_date:
        # ex = Exception('Date Exceeded')
        # raise ex

    return True


if __name__ == '__main__':
    result = license_verify()
    print('verify result:', result)
