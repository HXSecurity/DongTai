#!/usr/local/env python
# -*- coding: utf-8 -*-
import logging

from captcha.models import CaptchaStore
from django.contrib.auth import authenticate, login

from dongtai.endpoint import R
from dongtai.endpoint import UserEndPoint

logger = logging.getLogger("dongtai-webapi")
def decorator_factory(querys, request_body):
    def myextend_schema(func):
        import os
        if os.getenv('environment', None) == 'TEST':
            from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiTypes
            deco = extend_schema(
                parameters=[OpenApiParameter(**query) for query in querys],
                examples=[OpenApiExample('Example1', value=request_body)],
                request={'application/json': OpenApiTypes.OBJECT},
            )
            funcw = deco(func)
            funcw.querys = querys
            funcw.reqbody = request_body
            return funcw
        return func

    return myextend_schema
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiTypes


class UserLogin(UserEndPoint):
    """
    用户登录
    """
    permission_classes = []
    authentication_classes = []
    name = "user_views_login"
    description = "用户登录"

    @decorator_factory([], {
        'username': "",
        'password': "",
        'captcha_hash_key': "",
        'captcha': ""
    })
    def post(self, request):
        captcha_hash_key = request.data["captcha_hash_key"]
        captcha = request.data["captcha"]
        if captcha_hash_key and captcha:
            get_captcha = CaptchaStore.objects.get(hashkey=captcha_hash_key)
            # 如果验证码匹配
            if get_captcha.response == captcha.lower():
                username = request.data["username"]
                password = request.data["password"]
                user = authenticate(username=username, password=password)
                if user is not None and user.is_active:
                    login(request, user)
                    return R.success(msg='登录成功')
                else:
                    logger.warn(
                        f"user [{username}] login failure, rease: {'user not exist' if user is None else 'user is disable'}")
                    return R.failure(status=202, msg='登录失败')
            else:
                return R.failure(status=203, msg='验证码错误')
        else:
            return R.failure(status=204, msg='验证码不能为空')
