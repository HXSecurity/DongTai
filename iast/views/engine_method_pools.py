#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/28 上午11:32
# software: PyCharm
# project: lingzhi-webapi

from base.endpoint import SessionAuthProxyView
from dongtai.endpoint import UserPermission


class MethodPoolProxy(SessionAuthProxyView):
    permission_classes = (UserPermission,)
    source = 'api/engine/method_pools'
