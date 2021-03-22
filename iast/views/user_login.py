#!/usr/local/env python
# -*- coding: utf-8 -*-
import logging

from captcha.models import CaptchaStore
from django.contrib.auth import authenticate, login

from base import R
from iast.base.user import UserEndPoint

logger = logging.getLogger("django")


class UserLogin(UserEndPoint):
    """
    用户登录
    """
    permission_classes = []
    authentication_classes = []
    name = "user_views_login"
    description = "用户登录"

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
                    return R.failure(status=202, msg='登录失败')
            else:
                return R.failure(status=203, msg='验证码错误')
        else:
            return R.failure(status=204, msg='验证码不能为空')
