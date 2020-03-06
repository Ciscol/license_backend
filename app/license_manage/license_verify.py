import json
from app.rsa_manage.rsa_tool import decrypt, sign, get_publicKey, get_privateKey, sign_verify
from . import get_print


# 验证license
def license_verify():
    pubKey = get_publicKey()
    priKey = get_privateKey()
    curr_date = '2020-03-07'  # 应当获取当地时间 # 还要写一个date工具
    message = get_print()

    # 获取license数据
    with open('./license_data.json', 'r') as f:
        result = json.loads(f.read())
    print('license:', '\n', result, '\n')

    # 数字签名验证
    signature = result['license_data']['signature'].encode('utf-8')
    signature_message = result['license_data']['signature_message']
    verify = sign_verify(pubKey, signature, signature_message)
    if not verify:
        return 'Signature Error'

    # 密文验证
    crypto = result['license_data']['crypto'].encode('utf-8')
    try:
        decrypto = decrypt(priKey, crypto)
    except Exception:
        return 'Decryption Error'
    print('decrypto:', '\n', decrypto, '\n')
    if decrypto != message:
        return 'Message Error'

    # 有效期验证
    crypto = result['license_data']['valid_date'].encode('utf-8')
    valid_date = decrypt(priKey, crypto)
    print('valid_date:', '\n', valid_date, '\n')
    # if valid_date < curr_date:
    #     return 'Date Exceeded'

    return True


if __name__ == '__main__':
    result = license_verify()
    print('verify result:', result)
