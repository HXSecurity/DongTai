#!/usr/bin/env python

import logging

from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema

from dongtai_common.endpoint import R, UserEndPoint

logger = logging.getLogger("dongtai-webapi")


class UserPassword(UserEndPoint):
    name = "api-v1-user-password"
    description = _("Change Password")

    @extend_schema(
        summary=_("Change Password"),
        tags=[_("User")],
    )
    def post(self, request):
        user = request.user
        try:
            if not request.data["old_password"] or not request.data["new_password"]:
                return R.failure(msg=_("Password should not be empty"))
            user_check = authenticate(username=user.username, password=request.data["old_password"])
            if user_check is not None and user_check.is_active:
                password = request.data["new_password"]

                user.set_password(password)
                user.save(update_fields=["password"])
                return R.success(msg=_("Password has been changed successfully"))
            return R.failure(msg=_("Incorrect old password"))
        except Exception as e:
            logger.exception("uncatched exception: ", exc_info=e)
            return R.failure(msg=_("Incorrect"))
