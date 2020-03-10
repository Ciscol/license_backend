import base64
import json
import sys
import uuid
import wmi
import os
from hashlib import md5

path = os.path.dirname(__file__)
sysInfoFile = os.path.join(path, 'sys.info')

c = wmi.WMI()


# CPU
def getCPUid():
    cpus = []
    for cpu in c.Win32_Processor():
        item = {
            'ID': cpu.ProcessorId.strip()
        }
        cpus.append(item)
    return cpus


# Main Board
def getBaseboardSerialNumber():
    boards = []
    for board_id in c.Win32_BaseBoard():
        item = {
            'Serial Number': board_id.SerialNumber  # 主板序列号
        }
        boards.append(item)
    return boards


# Mac Address：
def getMac():
    node = uuid.getnode()
    mac = uuid.UUID(int=node).hex[-12:]
    return mac


# 信息写入文件
def create_sysInfo():
    # 设备指纹数据生成
    sysInfo = {
        'cpu': getCPUid(),
        'baseboardSerialNumber': getBaseboardSerialNumber(),
        'mac': getMac()
    }

    with open(sysInfoFile, 'w') as f:
        # json.dump(sysInfo, f, indent=4, separators=(',', ': '))
        json.dump(sysInfo, f)
    
    return sysInfo


# 获取设备指纹
def get_sysInfo():
    sysInfo = create_sysInfo()
    # with open(sysInfoFile, 'r') as f:
    #     result = md5(bytes(f.read(), 'utf-8')).hexdigest()
    # return result
    result = md5(bytes(str(sysInfo), 'utf-8')).hexdigest()
    return result

if __name__ == '__main__':
    create_sysInfo()
    # print(get_sysInfo())
