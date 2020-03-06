import rsa
import base64
import json


# 生成密钥
def create_keys():
    (pubKey, priKey) = rsa.newkeys(1024)
    print('keys create success!')
    print('public key:', pubKey)
    print('private key:', priKey)

    # 写入文件
    pub = pubKey.save_pkcs1()
    with open('public.pem', 'wb+')as f:
        f.write(pub)
    pri = priKey.save_pkcs1()
    with open('private.pem', 'wb+')as f:
        f.write(pri)


# 获取公钥
def get_publicKey():
    with open('public.pem', 'rb') as pubFile:
        pub = pubFile.read()
    pubKey = rsa.PublicKey.load_pkcs1(pub)
    return pubKey


# 获取私钥
def get_privateKey():
    with open('private.pem', 'rb') as priFile:
        pri = priFile.read()
    priKey = rsa.PrivateKey.load_pkcs1(pri)
    return priKey


# 公钥加密
def encrypt(publicKey, message):
    crypto = rsa.encrypt(message.encode('utf-8'), publicKey)
    return base64.b64encode(crypto)


# 签名
def sign(privateKey, message):
    signature = rsa.sign(message.encode('utf-8'), privateKey, 'SHA-1')

    # with open('signature_file.json', 'w') as f:
    #     f.write(json.dumps(str(signature)))
    # signature_str = json.dumps(str(signature), ensure_ascii=False)
    # print('signature_str:', signature_str)

    signature_b64 = base64.b64encode(signature)
    return signature_b64


# 签名验证
def sign_verify(publicKey, signature, message):
    try:
        signature = base64.b64decode(signature)
        method_name = rsa.verify(message.encode('utf-8'), signature, publicKey)
        # print('method_name:', method_name)
    except Exception:
        return False
    return True


# 私钥解密
def decrypt(privateKey, crypto):
    message = rsa.decrypt(base64.b64decode(crypto), privateKey).decode('utf-8')
    return message


if __name__ == '__main__':
    create_keys()
