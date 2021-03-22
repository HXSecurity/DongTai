#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/26 下午12:41
# software: PyCharm
# project: lingzhi-webapi
from base.endpoint import SessionAuthEndPoint
from iast.permissions import ScopedPermission


class SystemPermission(ScopedPermission):
    def has_permission(self, request, view):
        user = request.user
        if user is not None and user.is_system_admin():
            return True
        return False

    def has_object_permission(self, request, view, obj):
        print('enter has object permission')
        return super().has_object_permission(request, view, obj)


class SystemEndPoint(SessionAuthEndPoint):
    permission_classes = (SystemPermission,)