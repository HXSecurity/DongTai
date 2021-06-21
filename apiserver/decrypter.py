#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/12 下午7:49
# software: PyCharm
# project: lingzhi-agent-server
import gzip
import json

from apiserver.encrypter import RsaCrypto


def parse_data(stream_data):
    """从http request解析iast agent上报的json数据

    步骤：
        1.从http request对象读取二进制流
        2.gzip解压缩
        3.rsa解密
        4.json反序列化
    :param stream_data: POST请求的流式对象
    :return: iast agent上报的json数据，如果解压缩、解密过程失败，则抛出异常
    """
    data = gzip.decompress(stream_data).decode('utf-8')
    # fixme JavaAgent中RSA加密后数据无法在云端正常解密，导致部分漏洞无法检出，暂时关闭RSA加解密功能
    # data = RsaCrypto.decrypt(data)
    objs = json.loads(data)
    return objs
