#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/12/24 下午3:26
# software: PyCharm
# project: lingzhi-webapi
from captcha.models import CaptchaStore
from rest_framework.views import APIView

from base import R


class CaptchaVerify(APIView):
    def get(self, request):
        hash_key = request.query_params.get('key', None)
        captcha = request.query_params.get('captcha', None)
        status = 0
        if hash_key and captcha:
            get_captcha = CaptchaStore.objects.get(hashkey=hash_key)
            # 如果验证码匹配
            if get_captcha.response == captcha.lower():
                status = 1
        return R.success(data={'status': status})
