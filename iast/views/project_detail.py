#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/30 下午9:56
# software: PyCharm
# project: lingzhi-webapi

from base import R
from dongtai.utils import const
from iast.base.user import UserEndPoint
from dongtai.models.agent import IastAgent
from dongtai.models.project import IastProject
from dongtai.models.project_version import IastProjectVersion
from iast.base.project_version import get_project_version


class ProjectDetail(UserEndPoint):
    """
    创建用户，默认只能创建普通用户
    """
    name = "api-v1-project-<id>"
    description = "查看项目详情"

    def get(self, request, id):
        auth_users = self.get_auth_users(request.user)
        project = IastProject.objects.filter(user__in=auth_users, id=id).first()

        if project:
            relations = IastAgent.objects.filter(bind_project_id=project.id, is_running=const.RUNNING)
            agents = [{"id": relation.id, "name": relation.token} for relation in relations]
            if project.scan:
                scan_id = project.scan.id
            else:
                scan_id = 0
            # 获取项目当前版本信息
            current_project_version = get_project_version(project.id, auth_users)
            return R.success(data={
                "name": project.name,
                "id": project.id,
                "mode": project.mode,
                "scan_id": scan_id,
                "agents": agents,
                "versionData": current_project_version,
            })
        else:
            return R.failure(status=203, msg='no permission')
