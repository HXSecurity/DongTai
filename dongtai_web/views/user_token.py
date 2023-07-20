#!/usr/bin/env python
# datetime:2020/5/25 15:03
import logging

from dongtai_common.endpoint import R
from dongtai_common.endpoint import UserEndPoint
from rest_framework.authtoken.models import Token
from drf_spectacular.utils import extend_schema
from django.utils.translation import gettext_lazy as _
from dongtai_web.projecttemplate.update_department_data import update_department_data

logger = logging.getLogger("django")


class UserToken(UserEndPoint):
    name = "iast-v1-user-token"
    description = _("Get OpenAPI token")

    @extend_schema(
        summary=_("Get OpenAPI token"),
        tags=[_("User")],
    )
    def get(self, request):
        token, success = Token.objects.get_or_create(user=request.user)

        return R.success(data={"token": token.key})


class UserDepartmentToken(UserEndPoint):
    name = "iast-v1-user-department-token"
    description = _("获取部门部署 token")

    @extend_schema(
        summary=_("获取部门部署 token"),
        tags=[_("User")],
    )
    def get(self, request):
        departments = request.user.get_relative_department()
        department = request.user.get_department()
        if not department.token:
            update_department_data()
        tokens = departments.values("id", "token", "name").all()
        for token in tokens:
            token["token"] = "GROUP" + token["token"]
        return R.success(data=list(tokens))
