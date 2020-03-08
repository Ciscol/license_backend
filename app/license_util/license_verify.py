import json
from .get_print import get_print
from app.rsa_util.rsa_tool import decrypt, get_publicKey, get_privateKey, sign_verify
import os
path = os.path.dirname(__file__)
licenseFile = os.path.join(path, 'license_data.json')


# 验证license
def license_verify():
    pubKey = get_publicKey()
    priKey = get_privateKey()
    curr_date = '2020-03-07'  # 应当获取当地时间 # 还要写一个date工具
    message = get_print()

    # 获取license数据
    with open(licenseFile, 'r') as f:
        result = json.loads(f.read())
    print('license:', '\n', result, '\n')

    # 数字签名验证
    signature = result['license_data']['signature'].encode('utf-8')
    signature_message = result['license_data']['signature_message']
    verify = sign_verify(pubKey, signature, signature_message)
    if not verify:
        ex = Exception('Signature Error.')
        raise ex

    # 密文验证
    crypto = result['license_data']['crypto'].encode('utf-8')
    try:
        decrypto = decrypt(priKey, crypto)
    except Exception:
        ex = Exception('Message Decryption Error.')
        raise ex
    print('decrypto:', '\n', decrypto, '\n')
    if decrypto != message:
        ex = Exception('Message Error.')
        raise ex

    # 有效期验证
    crypto = result['license_data']['valid_date'].encode('utf-8')
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
