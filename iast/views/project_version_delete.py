#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:sjh
# datetime:2021/06/09 上午10:52
# software: PyCharm
# project: lingzhi-webapi
import logging, time
from base import R
from iast.base.user import UserEndPoint
from dongtai.models.project_version import IastProjectVersion

logger = logging.getLogger("django")


class ProjectVersionDelete(UserEndPoint):
    """
    删除项目版本信息
    """
    name = "api-v1-project-version-delete"
    description = "删除项目版本信息"

    def post(self, request):
        try:
            version_id = request.data.get("version_id", 0)
            project_id = request.data.get("project_id", 0)
            if not version_id or not project_id:
                return R.failure(status=202, msg='参数错误')
            version = IastProjectVersion.objects.filter(id=version_id, project_id=project_id, user=request.user, status=1).first()
            if version:
                version.status = 0
                version.update_time = int(time.time())
                version.save(update_fields=['status'])
                return R.success(msg='删除成功')
            else:
                return R.failure(status=202, msg='版本不存在')

        except Exception as e:
            return R.failure(status=202, msg=e)
