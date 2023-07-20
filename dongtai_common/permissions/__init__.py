#!/usr/bin/env python
# -*- coding:utf-8 -*-
# datetime: 2021/7/21 下午4:04

from rest_framework import permissions


class ScopedPermission(permissions.BasePermission):
    """
    Permissions work depending on the type of authentication:

    - A user inherits permissions based on their membership role. These are
      still dictated as common scopes, but they can't be checked until the
      has_object_permission hook is called.
    - ProjectKeys (legacy) are granted only project based scopes. This
    - APIKeys specify their scope, and work as expected.
    """

    scope_map = {
        "HEAD": (),
        "GET": (),
        "POST": (),
        "PUT": (),
        "PATCH": (),
        "DELETE": (),
    }

    def has_permission(self, request, view):
        # session-based auth has all scopes for a logged in user
        if not getattr(request, "auth", None):
            return request.user.is_authenticated()

        allowed_scopes = set(self.scope_map.get(request.method, []))
        current_scopes = request.auth.get_scopes()
        return any(s in allowed_scopes for s in current_scopes)

    def has_object_permission(self, request, view, obj):
        return False


class UserPermission(ScopedPermission):
    """
    用户权限验证类,验证是否为有效用户
    """

    def has_permission(self, request, view):
        user = request.user
        if user is not None and user.is_active:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        print("enter has object permission")
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
        print("enter has object permission")
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
        print("enter has object permission")
        return super().has_object_permission(request, view, obj)
