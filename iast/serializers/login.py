#!/usr/local/env python
# -*- coding: utf-8 -*-
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    """
    验证器类的属性详情参考
    https://www.django-rest-framework.org/api-guide/fields/
    """
    username = serializers.CharField(
        required=True,
        max_length=12,
        error_messages={
            "username": "用户名不能为空"
        }
    )
    password = serializers.CharField(
        required=True,
        max_length=6,
        error_messages={
            "password": "密码不能为空"
        }
    )
