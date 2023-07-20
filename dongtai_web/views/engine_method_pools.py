#!/usr/bin/env python
# -*- coding:utf-8 -*-

from base.endpoint import SessionAuthProxyView
from dongtai_common.endpoint import UserPermission


class MethodPoolProxy(SessionAuthProxyView):
    permission_classes = (UserPermission,)
    source = "api/engine/method_pools"
