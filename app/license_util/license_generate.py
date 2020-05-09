import json
from .sysInfo import get_sysInfo
from app.crypto_util import rsa_tool, tripleDES_tool
from datetime import datetime, timedelta
import os

path = os.path.dirname(__file__)
licenseFile = os.path.join(path, 'license.lic')


# 生成licence
def license_generate(username='', valid_seconds=60, modules=None):
    if modules is None:
        modules = []
    try:
        priKey = rsa_tool.get_privateKey()

        # 获取设备指纹
        sysInfo = get_sysInfo()

        # 计算、加密有效期限
        valid_date = date_adder(valid_seconds)
        valid_date = tripleDES_tool.encrypt(valid_date, sysInfo[::2])
        valid_date = str(valid_date, 'utf-8')

        # 授权模块
        modules = str(modules)

        # licence part1 —— 主体内容
        content = {
            'username': username,
            'host_features': sysInfo,
            'valid_date': valid_date,
            'authorized_modules': modules
        }

        # licence part2 —— 数字签名
        signature = str(rsa_tool.sign(priKey, str(content)), 'utf-8')

        # license数据生成并写入文件
        license_data = {
            'license': content,
            'signature': signature
        }
        with open(licenseFile, 'w') as f:
            json.dump(license_data, f, indent=4, separators=(',', ': '))
    except Exception as ex:
        raise ex
    return True


def date_adder(valid_seconds):
    return datetime.strftime(datetime.now() + timedelta(seconds=valid_seconds), '%Y-%m-%d %H: %M: %S')
