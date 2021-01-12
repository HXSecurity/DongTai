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

from M2Crypto import BIO, RSA

from AgentServer import settings

with open(settings.PRIVATE_KEY, 'r') as f:
    PRIVATE_KEY = f.read()


class RsaCrypto:
    MAX_LENGTH = 128

    @staticmethod
    def cut(data, length):
        return [data[i:i + length] for i in range(0, len(data), length)]

    @staticmethod
    def decrypt(encrypt_data):
        # 解密
        cipher = base64.b64decode(encrypt_data)
        ciphers = RsaCrypto.cut(cipher, RsaCrypto.MAX_LENGTH)
        pri_bio = BIO.MemoryBuffer(PRIVATE_KEY.encode('utf-8'))
        pri_rsa = RSA.load_key_bio(pri_bio)
        fragments = []
        for _cipher in ciphers:
            plain = pri_rsa.private_decrypt(_cipher, RSA.pkcs1_padding)
            fragments.append(plain.decode('utf-8'))
        return ''.join(fragments)

    @staticmethod
    def encrypt(data):
        with open(settings.PUBLIC_KEY, 'r') as public_key:
            public_key_value = public_key.read()
        text = data.encode('utf-8')
        fragments = RsaCrypto.cut(text, 118)
        pub_bio = BIO.MemoryBuffer(public_key_value.encode('utf-8'))
        pub_rsa = RSA.load_pub_key_bio(pub_bio)

        secret = bytes()
        for fragment in fragments:
            secret += pub_rsa.public_encrypt(fragment, RSA.pkcs1_padding)
        sign = base64.b64encode(secret)
        return sign.decode('utf-8')
