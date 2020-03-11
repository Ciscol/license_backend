import json
from .sysInfo import get_sysInfo
from app.rsa_util.rsa_tool import encrypt, sign, get_publicKey, get_privateKey
from hashlib import md5
from datetime import datetime, timedelta
import os

path = os.path.dirname(__file__)
licenseFile = os.path.join(path, 'license_data.json')


# 生成license
def license_generate(valid_seconds=60):
    try:
        pubKey = get_publicKey()
        priKey = get_privateKey()

        # 设备指纹
        sysInfo = encrypt(pubKey, get_sysInfo())

        # 应当为当地时间 + 有效时长(seconds)
        valid_date = datetime.strftime(datetime.now() + timedelta(seconds=valid_seconds), '%Y-%m-%d %H: %M: %S')
        valid_date = encrypt(pubKey, valid_date)

        content = {
            'sysInfo': str(sysInfo, 'utf-8'),
            'valid_date': str(valid_date, 'utf-8')
        }

        # 数字签名,用户使用公钥进行解密比对,用于验证license来源
        signature = str(sign(priKey, str(content)), 'utf-8')
        # print('signature:', '\n', str(signature, 'utf-8'), '\n')

        # license数据生成
        license_data = {
            'content': content,
            'signature': signature
        }

        with open(licenseFile, 'w') as f:
            # json.dump(license_data, f, indent=4, separators=(',', ': '))
            json.dump(license_data, f)
        print('license:', '\n', license_data)
        return True
    except Exception as ex:
        raise ex


if __name__ == '__main__':
    license_generate()
