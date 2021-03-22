#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/26 下午12:40
# software: PyCharm
# project: lingzhi-webapi
from base.endpoint import AnonymousAuthEndPoint, SessionAuthEndPoint
from iast.permissions import ScopedPermission


class ScaPermission(ScopedPermission):
    def has_permission(self, request, view):
        user = request.user
        if user is not None and user.is_active:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        print('enter has object permission')
        return super().has_object_permission(request, view, obj)


class ScaEndPoint(SessionAuthEndPoint):
    permission_classes = (ScaPermission,)
