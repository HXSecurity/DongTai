#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:sjh
# software: PyCharm
# project: lingzhi-webapi
import logging

from dongtai.endpoint import R
from dongtai.endpoint import UserEndPoint

from iast.base.project_version import version_modify
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger("django")


class ProjectVersionAdd(UserEndPoint):
    name = "api-v1-project-version-add"
    description = _("New project version information")

    def post(self, request):
        try:
            result = version_modify(request.user, request.data)
            if result.get("status", "202") == "202":
                return R.failure(status=202, msg=_("Parameter error"))
            else:
                return R.success(msg=_('Create success'), data=result.get("data", {}))

        except Exception as e:
            return R.failure(status=202, msg=e)
