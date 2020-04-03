import json
from .sysInfo import get_sysInfo
from app.crypto_util import rsa_tool, des3_tool
from datetime import datetime, timedelta
import os

path = os.path.dirname(__file__)
licenseFile = os.path.join(path, 'license.lic')


# 生成license
def license_generate(username='', valid_seconds=60, modules=None):
    if modules is None:
        modules = []
    try:
        priKey = rsa_tool.get_privateKey()

        # 设备指纹
        sysInfo = get_sysInfo()

        # 有效时长
        valid_date = date_adder(valid_seconds)
        valid_date = des3_tool.encrypt(valid_date)
        valid_date = str(valid_date, 'utf-8')

        # 模块
        modules = str(modules)

        # license part1 —— 主体内容
        content = {
            'username': username,
            'sysInfo': sysInfo,
            'valid_date': valid_date,
            'valid_modules': modules
        }

        # license part2 —— 数字签名
        signature = str(rsa_tool.sign(priKey, str(content)), 'utf-8')

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
