#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi

from base.endpoint import SessionAuthProxyView
from dongtai_common.endpoint import UserPermission


class MethodPoolProxy(SessionAuthProxyView):
    permission_classes = (UserPermission,)
    source = "api/engine/method_pools"
