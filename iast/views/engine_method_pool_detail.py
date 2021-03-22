#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/28 上午11:32
# software: PyCharm
# project: lingzhi-webapi

from base.endpoint import AnonymousAuthProxyView, SessionAuthProxyView


class MethodPoolDetailProxy(SessionAuthProxyView):
    source = 'api/engine/method_pool/detail'
