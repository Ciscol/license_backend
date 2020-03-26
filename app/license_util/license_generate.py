import json
from .sysInfo import get_sysInfo
from app.rsa_util.rsa_tool import encrypt, sign, get_publicKey, get_privateKey
from datetime import datetime, timedelta
import os

path = os.path.dirname(__file__)
licenseFile = os.path.join(path, 'license.data')


# 生成license
def license_generate(username='', valid_seconds=60, modules=None):
    if modules is None:
        modules = []
    try:
        pubKey = get_publicKey()
        priKey = get_privateKey()

        # 用户名
        username = encrypt(pubKey, username)

        # 设备指纹
        sysInfo = encrypt(pubKey, get_sysInfo())

        # 有效时长
        valid_date = date_adder(valid_seconds)
        valid_date = encrypt(pubKey, valid_date)

        # 模块
        modules = encrypt(pubKey, str(modules))

        # license part1 —— 主体内容
        content = {
            'username': str(username, 'utf-8'),
            'sysInfo': str(sysInfo, 'utf-8'),
            'valid_date': str(valid_date, 'utf-8'),
            'valid_modules': str(modules, 'utf-8')
        }

        # license part2 —— 数字签名
        signature = str(sign(priKey, str(content)), 'utf-8')

        # license数据生成并写入文件
        license_data = {
            'content': content,
            'signature': signature
        }
        with open(licenseFile, 'w') as f:
            json.dump(license_data, f, indent=4, separators=(',', ': '))
            # json.dump(license_data, f)
        # print('license:', '\n', license_data)
        return True
    except Exception as ex:
        raise ex


def date_adder(valid_seconds):
    return datetime.strftime(datetime.now() + timedelta(seconds=valid_seconds), '%Y-%m-%d %H: %M: %S')


if __name__ == '__main__':
    license_generate()
