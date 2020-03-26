import json
import time
from datetime import datetime
from .sysInfo import get_sysInfo
from app.rsa_util.rsa_tool import decrypt, get_publicKey, get_privateKey, sign_verify
import os

path = os.path.dirname(__file__)
licenseFile = os.path.join(path, 'license.data')


# 验证license
def license_verify():
    pubKey = get_publicKey()
    priKey = get_privateKey()

    # 设备指纹
    sysInfo = get_sysInfo()

    # 获取license数据
    with open(licenseFile, 'r') as f:
        result = json.loads(f.read())
    print('license:', '\n', result, '\n')

    license_content = result['content']
    license_signature = result['signature']
    license_sysInfo = license_content['sysInfo']
    license_username = license_content['username']
    license_valid_date = license_content['valid_date']
    license_modules = license_content['valid_modules']

    # 数字签名验证
    verification = sign_verify(pubKey, license_signature, str(license_content))
    if not verification:
        ex = Exception('Signature Error.')
        raise ex

    # 设备指纹验证
    crypto = license_sysInfo.encode('utf-8')
    try:
        decrypto = decrypt(priKey, crypto)
    except Exception:
        ex = Exception('SysInfo Decryption Error.')
        raise ex
    print('decrypto:', '\n', decrypto, '\n')
    if decrypto != sysInfo:
        ex = Exception('SysInfo Error.')
        raise ex

    # 有效期验证
    crypto = license_valid_date.encode('utf-8')
    try:
        valid_date = decrypt(priKey, crypto)
    except Exception:
        ex = Exception('Valid-Date Decryption Error.')
        raise ex
    try:
        if not is_valid_date(valid_date):
            ex = Exception('Date Expired')
            raise ex
    except Exception as ex:
        raise ex

    # 有效模块
    license_modules = license_modules.encode('utf-8')
    try:
        license_modules = decrypt(priKey, license_modules)
    except Exception:
        ex = Exception('Modules Decryption Error.')
        raise ex
    license_modules = json.loads(license_modules.replace("'", "\""))

    # 用户名
    license_username = license_username.encode('utf-8')
    try:
        license_username = decrypt(priKey, license_username)
    except Exception:
        ex = Exception('username Decryption Error.')
        raise ex

    return {'username': license_username, 'modules': license_modules, 'valid_date': valid_date}


def is_valid_date(timestr):
    # 获取当前时间日期
    nowTime_str = datetime.now().strftime('%Y-%m-%d %H: %M: %S')
    print(nowTime_str)
    print(timestr)
    e_time = time.mktime(time.strptime(nowTime_str, '%Y-%m-%d %H: %M: %S'))
    print(e_time)
    try:
        s_time = time.mktime(time.strptime(timestr, '%Y-%m-%d %H: %M: %S'))
        print(s_time)
        # 日期转化为int比较
        diff = int(s_time) - int(e_time)
        print(diff)
        if diff >= 0:
            return True
        else:
            return False
    except Exception as ex:
        raise ex


if __name__ == '__main__':
    result = license_verify()
    print('verify result:', result)
