#!/usr/bin/env python
from captcha.models import CaptchaStore
from rest_framework.views import APIView

from dongtai_common.endpoint import R


class CaptchaVerify(APIView):
    def get(self, request):
        hash_key = request.query_params.get("key", None)
        captcha = request.query_params.get("captcha", None)
        status = 0
        if hash_key and captcha:
            get_captcha = CaptchaStore.objects.get(hashkey=hash_key)

            if get_captcha.response == captcha.lower():
                status = 1
        return R.success(data={"status": status})
