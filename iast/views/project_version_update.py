#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:sjh
# software: PyCharm
# project: lingzhi-webapi
import logging

from dongtai.endpoint import R
from iast.base.project_version import version_modify
from dongtai.endpoint import UserEndPoint
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger("django")


class ProjectVersionUpdate(UserEndPoint):
    name = "api-v1-project-version-update"
    description = _("Update project version information")

    def post(self, request):
        try:
            version_id = request.data.get("version_id", 0)
            result = version_modify(request.user, request.data)
            if not version_id or result.get("status", "202") == "202":
                return R.failure(status=202, msg=_("Parameter error"))
            else:
                return R.success(msg=_('update completed'))

        except Exception as e:
            return R.failure(status=202, msg=_('Program error'))
