#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/25 上午10:10
# software: PyCharm
# project: sentry
from vuln.permissions import ScopedPermission


class UserPermission(ScopedPermission):
    def has_permission(self, request, view):
        user = request.user
        if user is not None and user.is_active:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        print('enter has object permission')
        return super().has_object_permission(request, view, obj)


class TalentAdminPermission(ScopedPermission):
    def has_permission(self, request, view):
        user = request.user
        if user is not None and user.is_active and user.is_talent_admin():
            return True
        return False

    def has_object_permission(self, request, view, obj):
        print('enter has object permission')
        return super().has_object_permission(request, view, obj)


class SystemAdminPermission(ScopedPermission):
    def has_permission(self, request, view):
        user = request.user
        if user is not None and user.is_active and user.is_system_admin():
            return True
        return False

    def has_object_permission(self, request, view, obj):
        print('enter has object permission')
        return super().has_object_permission(request, view, obj)
