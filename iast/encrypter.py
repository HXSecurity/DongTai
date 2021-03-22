#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/6/4 14:55
# software: PyCharm
# project: webapi

"""
RSA加解密
"""
import base64
import os

from M2Crypto import BIO, RSA

basedir = os.path.dirname(os.path.realpath(__file__))
private_key_file = os.path.join(basedir, "private_key.pem")  # 读取私钥
with open(private_key_file, 'r') as f:
    PRIVATE_KEY = f.read()

class RsaCrypto:
    MAX_LENGTH = 128

    @staticmethod
    def cut(data, length):
        return [data[i:i + length] for i in range(0, len(data), length)]

    @staticmethod
    def decrypt(encrypt_data):
        # 解密
        cipher = base64.b64decode(encrypt_data)  # base64解码
        ciphers = RsaCrypto.cut(cipher, RsaCrypto.MAX_LENGTH)
        pri_bio = BIO.MemoryBuffer(PRIVATE_KEY.encode('utf-8'))  # 加载私钥
        pri_rsa = RSA.load_key_bio(pri_bio)
        datas = []
        for _cipher in ciphers:
            plain = pri_rsa.private_decrypt(_cipher, RSA.pkcs1_padding)  # 解密
            datas.append(plain.decode('utf-8'))
        return ''.join(datas)

    @staticmethod
    def encrypt(data):
        # 加密
        with open("/tmp/public_key.pem", 'r') as f:
            PUBLIC_KEY = f.read()
        text = data.encode('utf-8')  # 明文
        datas = RsaCrypto.cut(text, 118)
        pub_bio = BIO.MemoryBuffer(PUBLIC_KEY.encode('utf-8'))  # 公钥字符串
        pub_rsa = RSA.load_pub_key_bio(pub_bio)  # 加载公钥

        secret = bytes()
        for data in datas:
            secret += pub_rsa.public_encrypt(data, RSA.pkcs1_padding)  # 公钥加密
        sign = base64.b64encode(secret)  # 密文base64编码
        return sign.decode('utf-8')


if __name__ == "__main__":
    str = RsaCrypto.encrypt("hello")
    print("加密后密文：%s" % str)
    content = RsaCrypto.decrypt(str)
    print("解密后明文：%s" % content)
    # str = "GqJZL2LiW4+O9ey9Q5WEZMDCC9TvWft5euLFx8LvFwYn1BhOg7zjvzOy0oLnhCT3z6t7ZMpdStikPmQVF2bqNloG3PTiUXG7oyz0wxEnH0YG7HPQBS3gTj5/u08O0n8SHHyjyMjZId5w5XuHhRcld6iEjWXXqCAqT4mWn5MllDc="
    # content = RsaCrypto.decrypt(str)
    # print("解密后明文：%s" % content)
    str = "lYtVGEGJscyObxNgBHDrlgkjvme0SSnwnXzQDrM3LuIznYCA3oltTK9tUvz60KW2Df35j5OeX0YPU94skYhSV0bSHtb5iDe7M0fIU+jbi05pYlaDpynpw8bXTrjKdxyTzxMd7z1MECMiuCSNWwa9DzqUkQWSf+LePB8jK3LAHpB4IRh7cnCHqZQgnWQlHwPNqU376LFUQeTgBFEb2fR2sOohFQdHUKq5YLahtnhVMtyEovQ66HZbEk03hBMJd6lqPGZ1UCVyujZYj3+5mK+ntU6bbyqZIKEgktqUqhtyJT6L6Gd1MxUdGWsZ7hgBjT5DgXBGBAcwzu/CQPcnmLS9ezw/3D+cBmcu3l6x4dYrqya5Xoe9u7TQjtymozcPROKnyIAtB+R3vkPP2xyjb9Ae1qbpNEcze64eEYCQgJeUw8QjlVfNduhFUKqo01ThhHH93d2oxshw4kmPwGwqWdhvdXaaoAamn/+Y71+OXSxPXzIMxruTlkGXtMYteaBzPVPmYH1sKfWrhlCx2TrTy4GcQ6LlYEO9VLT+zXFbIZTR8Sad+BLt9PRig+tukPZ6TRt6yYp9c+a5VbypFnsuN1Qn48/Bz/mIKjvP7aWXoVPUXMmf+GRGrm5Qk7An9dLD/tBv/uZXYIpE/3p4JNgeTPL0eJhH1K99qZbJFJT5vHzlMok="
    content = RsaCrypto.decrypt(str)
    print("解密后明文：%s" % content)
