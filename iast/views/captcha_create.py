#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/12/24 下午3:26
# software: PyCharm
# project: lingzhi-webapi
from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from rest_framework.views import APIView

from base import R


class CaptchaCreate(APIView):
    def get(self, request):
        hash_key = CaptchaStore.generate_key()
        image_url = captcha_image_url(hash_key)
        return R.success(data={'hash_key': hash_key, 'image_url': image_url})
