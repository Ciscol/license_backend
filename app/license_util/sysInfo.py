import uuid
from hashlib import md5


# Mac 地址：
def getMac():
    address = hex(uuid.getnode())[2:]
    mac = '-'.join(address[i:i + 2] for i in range(0, len(address), 2))
    return mac


# 获取设备硬件信息
def create_sysInfo():
    sysInfo = {
        'mac': getMac()
    }
    return sysInfo


# 获取设备指纹
def get_sysInfo():
    sysInfo = create_sysInfo()
    result = md5(bytes(str(sysInfo), 'utf-8')).hexdigest()
    return result
