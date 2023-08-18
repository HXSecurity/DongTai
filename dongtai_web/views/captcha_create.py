#!/usr/bin/env python
from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from rest_framework.views import APIView

from dongtai_common.endpoint import R


class CaptchaCreate(APIView):
    def get(self, request):
        hash_key = CaptchaStore.generate_key()
        image_url = captcha_image_url(hash_key)
        return R.success(data={"hash_key": hash_key, "image_url": image_url})
