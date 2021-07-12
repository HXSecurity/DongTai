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


class ProjectVersionList(UserEndPoint):
    """
    查看项目版本列表
    """
    name = "api-v1-project-version-list"
    description = "查看项目版本列表"

    def get(self, request, project_id):
        try:
            auth_users = self.get_auth_users(request.user)
            versionInfo = IastProjectVersion.objects.filter(project_id=project_id, user__in=auth_users, status=1).order_by("-id")
            data = []
            if versionInfo:
                for item in versionInfo:
                    data.append({
                        "version_id": item.id,
                        "version_name": item.version_name,
                        "current_version": item.current_version,
                        "description": item.description,
                    })
            return R.success(msg='查询成功', data=data)
        except Exception as e:
            return R.failure(status=202, msg=e)
