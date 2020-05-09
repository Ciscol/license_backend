import json
import time
from datetime import datetime
from .sysInfo import get_sysInfo
from app.crypto_util import rsa_tool, tripleDES_tool
import os

path = os.path.dirname(__file__)
licenseFile = os.path.join(path, 'license.lic')


# 验证licence
def license_verify():
    pubKey = rsa_tool.get_publicKey()

    # 获取设备指纹
    sysInfo = get_sysInfo()

    # 获取licence数据
    try:
        with open(licenseFile, 'r') as f:
            result = json.loads(f.read())
        print('license:', '\n', result, '\n')
    except Exception:
        ex = Exception('License error. No license file exist. ')
        raise ex

    license_content = result['license']
    license_signature = result['signature']
    license_sysInfo = license_content['host_features']
    license_username = license_content['username']
    license_valid_date = license_content['valid_date']
    license_modules = license_content['authorized_modules']

    # 数字签名验证
    try:
        verification = rsa_tool.sign_verify(pubKey, license_signature, str(license_content))
    except Exception:
        ex = Exception('Signature Error.')
        raise ex

    # 设备指纹验证
    if license_sysInfo != sysInfo:
        ex = Exception('System Info Error.')
        raise ex

    # 有效期限验证
    license_valid_date = license_valid_date.encode('utf-8')
    try:
        valid_date = tripleDES_tool.decrypt(license_valid_date, sysInfo[::2])
        valid_date = str(valid_date, 'utf-8')
    except Exception:
        ex = Exception('Valid-Date Decryption Error.')
        raise ex
    try:
        if not is_valid_date(valid_date):
            ex = Exception('License Expired')
            raise ex
    except Exception as ex:
        raise ex

    # 授权模块信息
    license_modules = json.loads(license_modules.replace("'", "\""))

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
