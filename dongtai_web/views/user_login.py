#!/usr/local/env python
import logging
import time

from captcha.models import CaptchaStore
from django.contrib.auth import authenticate, login
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.user import User

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
                    if user is not None:
                        login(request, user)
                        return R.success(
                            msg=_("Login successful"),
                            data={
                                "default_language": user.default_language,
                                "is_active": user.is_active,
                            },
                        )
                    user_login = User.objects.filter(username=username).first()
                    if user_login and not user_login.is_active:
                        return R.failure(
                            status=205,
                            msg="用户已被禁用",
                            data={
                                "default_language": user_login.default_language,
                                "is_active": user_login.is_active,
                            },
                        )
                    logger.warn(
                        f"user [{username}] login failure, rease: {'user not exist' if user is None else 'user is disable'}"
                    )
                    return R.failure(status=202, msg=_("Login failed"))
                return R.failure(status=203, msg=_("Verification code error"))
            return R.failure(status=204, msg=_("verification code should not be empty"))
        except Exception as e:
            logger.exception("uncatched exception: ", exc_info=e)
            return R.failure(status=202, msg=_("Login failed"))
