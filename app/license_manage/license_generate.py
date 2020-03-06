import json
from . import get_print
from app.rsa_manage.rsa_tool import encrypt, sign, get_publicKey, get_privateKey


# 生成license
def license_generate():
    pubKey = get_publicKey()
    priKey = get_privateKey()
    valid_date = encrypt(pubKey, '2020-03-08')  # 应当为当地时间 + 有效时长

    # message应当是设备指纹,由发证方使用公钥加密生成
    # 在验证license有效性时使用私钥解密,并与实时采集设备指纹进行比对
    message = get_print.get_print()
    crypto = encrypt(pubKey, message)
    print('crypto:', '\n', str(crypto, 'utf-8'), '\n')

    # 数字签名,用户使用公钥进行解密比对,用于验证license来源
    signature = sign(priKey, 'signature message')
    print('signature:', '\n', str(signature, 'utf-8'), '\n')

    # license数据生成
    license_data = {}
    license_data['crypto'] = str(crypto, 'utf-8')
    license_data['signature'] = str(signature, 'utf-8')
    license_data['publicKey'] = str(pubKey)
    license_data['valid_date'] = str(valid_date, 'utf-8')
    license_data['signature_message'] = 'signature message'
    result = {'license_data': license_data}

    with open('./license_data.json', 'w') as f:
        # json.dump(result, f, indent=4, separators=(',', ': '))
        json.dump(result, f)
    print('license:', '\n', result)


if __name__ == '__main__':
    license_generate()
