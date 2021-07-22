#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/2/18 上午9:41
# software: PyCharm
# project: lingzhi-engine
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature

from dongtai.endpoint import EndPoint, R

"""
Django内置签名的计算方法：
1.sale+secret，哈希计算key，利用key和待加密数据进行hmac计算，得到hmac散列数据
2.对hmac散列数据进行base64编码

签名验证方法：


设计的类及方法：
- django.core.signing
"""


class RunSigner(EndPoint):
    name = "api-engine-signer"
    description = "引擎创建签名"
    signer = TimestampSigner(sep='@')

    def get(self, request):
        import time
        timestamp = time.time()
        value = self.signer.sign(f'hello{timestamp}')
        print(value)
        return R.success(data={'sign': value})

    def post(self, request):
        # 接收
        signature = request.query_params.get('sign')
        print(signature)
        try:
            value = self.signer.unsign(signature, max_age=30)
            return R.success()
        except SignatureExpired as e:
            return R.failure(msg='签名已过期')
        except BadSignature as e:
            return R.failure(msg='签名无效')
