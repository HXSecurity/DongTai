#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:sjh
# datetime:2021/06/09 上午10:52
# software: PyCharm
# project: lingzhi-webapi
import logging

from base import R
from iast.base.project_version import version_modify
from iast.base.user import UserEndPoint

logger = logging.getLogger("django")


class ProjectVersionUpdate(UserEndPoint):
    """
    更新项目版本名称，描述
    """
    name = "api-v1-project-version-update"
    description = "更新项目版本信息"

    def post(self, request):
        try:
            version_id = request.data.get("version_id", 0)
            result = version_modify(request.user, request.data)
            if not version_id or result.get("status", "202") == "202":
                return R.failure(status=202, msg=result.get("msg", "参数错误"))
            else:
                return R.success(msg='更新成功')

        except Exception as e:
            return R.failure(status=202, msg=e)
