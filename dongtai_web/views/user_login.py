#!/usr/local/env python
import logging

from captcha.models import CaptchaStore
from django.contrib.auth import authenticate, login
from dongtai_web.utils import extend_schema_with_envcheck
from dongtai_common.endpoint import R
from dongtai_common.endpoint import UserEndPoint
from django.utils.translation import gettext_lazy as _
from dongtai_web.projecttemplate.update_department_data import update_department_data
import time
from drf_spectacular.utils import extend_schema

logger = logging.getLogger("dongtai-webapi")


class UserLogin(UserEndPoint):
    permission_classes = []
    authentication_classes = []
    name = "user_views_login"
    description = _("User login")

    @extend_schema(
        summary=_("User login"),
        tags=[_("User")],
    )
    def post(self, request):
        """{
        'username': "",
        'password': "",
        'captcha_hash_key': "",
        'captcha': ""
        }
        """
        try:
            captcha_hash_key = request.data["captcha_hash_key"]
            captcha = request.data["captcha"]
            if captcha_hash_key and captcha:
                captcha_obj = CaptchaStore.objects.get(hashkey=captcha_hash_key)
                if int(captcha_obj.expiration.timestamp()) < int(time.time()):
                    return R.failure(status=203, msg=_("Captcha timed out"))
                if captcha_obj.response == captcha.lower():
                    username = request.data["username"]
                    password = request.data["password"]
                    user = authenticate(username=username, password=password)
                    if user is not None and user.is_active:
                        login(request, user)
                        department = user.get_department()
                        if not department.department_path:
                            update_department_data()
                        return R.success(
                            msg=_("Login successful"),
                            data={"default_language": user.default_language},
                        )
                    else:
                        logger.warn(
                            f"user [{username}] login failure, rease: {'user not exist' if user is None else 'user is disable'}"
                        )
                        return R.failure(status=202, msg=_("Login failed"))
                else:
                    return R.failure(status=203, msg=_("Verification code error"))
            else:
                return R.failure(
                    status=204, msg=_("verification code should not be empty")
                )
        except Exception as e:
            logger.error(e)
            return R.failure(status=202, msg=_("Login failed"))
