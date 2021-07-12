#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:sjh
# datetime:2021/06/09 上午10:52
# software: PyCharm
# project: lingzhi-webapi
import logging, time
from base import R
from django.db.models import Q
from iast.base.user import UserEndPoint
from dongtai.models.project_version import IastProjectVersion
from dongtai.models.agent import IastAgent

logger = logging.getLogger("django")


class ProjectVersionCurrent(UserEndPoint):
    """
    将当前版本设置为项目在用版本
    """
    name = "api-v1-project-version-current"
    description = "设置为当前项目版本"

    def post(self, request):
        try:
            project_id = request.data.get("project_id", 0)
            version_id = request.data.get("version_id", 0)
            if not version_id or not project_id:
                return R.failure(status=202, msg='参数错误')

            # 重置项目版本
            version = IastProjectVersion.objects.filter(project_id=project_id, id=version_id, user=request.user).first()
            if version:
                version.current_version = 1
                version.update_time = int(time.time())
                version.save(update_fields=["current_version", "update_time"])
                IastAgent.objects.filter(user=request.user, bind_project_id=project_id, project_version_id=version_id).update(online=1)
                # 置空之前项目设置版本
                IastAgent.objects.filter(~Q(project_version_id=version_id), user=request.user, bind_project_id=project_id).update(online=0)
                IastProjectVersion.objects.filter(
                    ~Q(id=version_id),
                    project_id=project_id,
                    user=request.user,
                    current_version=1,
                    status=1
                ).update(current_version=0, update_time=int(time.time()))

                return R.success(msg='版本设置成功')
            else:
                return R.failure(status=202, msg='版本不存在')

        except Exception as e:
            return R.failure(status=202, msg="版本设置失败")
