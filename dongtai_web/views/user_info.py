#!/usr/bin/env python

import logging

from django.contrib.auth.models import Group

from dongtai_common.endpoint import R
from dongtai_common.endpoint import UserEndPoint
from django.utils.translation import gettext_lazy as _
from dongtai_conf.settings import SCA_SETUP
from drf_spectacular.utils import extend_schema

logger = logging.getLogger("django")


class UserInfoEndpoint(UserEndPoint):
    name = "api-v1-user-info"
    description = _("User Info")

    @extend_schema(
        summary=_("User Info"),
        tags=[_("User")],
    )
    def get(self, request):
        user = request.user
        group = Group.objects.filter(user=user).order_by("-id").first()

        return R.success(
            data={
                "userid": user.id if not user.is_anonymous else -1,
                "username": user.get_username(),
                "role": 3
                if group is None
                else 2
                if group.name == "talent_admin"
                else 1
                if group.name == "system_admin"
                else 0,
                "role_name": "" if group is None else group.name,
                "sca_setup": not SCA_SETUP,
            }
        )
