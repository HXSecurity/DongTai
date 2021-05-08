#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/30 下午9:56
# software: PyCharm
# project: lingzhi-webapi

from base import R
from iast.base.user import UserEndPoint
from dongtai_models.models.agent import IastAgent
from dongtai_models.models.project import IastProject


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
            relations = IastAgent.objects.filter(bind_project_id=project.id)
            agents = [{"id": relation.id, "name": relation.token} for relation in relations]
            if project.scan:
                scan_id = project.scan.id
            else:
                scan_id = 0
            return R.success(data={
                "name": project.name,
                "id": project.id,
                "mode": project.mode,
                "scan_id": scan_id,
                "agents": agents,
            })
        else:
            return R.failure(status=203, msg='no permission')
