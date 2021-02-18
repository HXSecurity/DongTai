#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/25 上午10:10
# software: PyCharm
from vuln.permissions import ScopedPermission


class UserPermission(ScopedPermission):
    """
    用户权限验证类，验证是否为有效用户
    """

    def has_permission(self, request, view):
        user = request.user
        if user is not None and user.is_active:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        print('enter has object permission')
        return super().has_object_permission(request, view, obj)


class TalentAdminPermission(ScopedPermission):
    """
    租户管理员权限验证类
    """

    def has_permission(self, request, view):
        user = request.user
        if user is not None and user.is_active and user.is_talent_admin():
            return True
        return False

    def has_object_permission(self, request, view, obj):
        print('enter has object permission')
        return super().has_object_permission(request, view, obj)


class SystemAdminPermission(ScopedPermission):
    """
    系统管理员权限验证类
    """

    def has_permission(self, request, view):
        user = request.user
        if user is not None and user.is_active and user.is_system_admin():
            return True
        return False

    def has_object_permission(self, request, view, obj):
        print('enter has object permission')
        return super().has_object_permission(request, view, obj)
