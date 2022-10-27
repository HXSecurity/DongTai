#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi

from base.endpoint import SessionAuthProxyView
from dongtai_common.endpoint import UserPermission


from _typeshed import Incomplete
class MethodPoolProxy(SessionAuthProxyView):
    permission_classes: Incomplete = (UserPermission,)
    source: str = 'api/engine/method_pools'
