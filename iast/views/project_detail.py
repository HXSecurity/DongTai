#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi

from dongtai.endpoint import R
from dongtai.endpoint import UserEndPoint
from dongtai.models.agent import IastAgent
from dongtai.models.project import IastProject
from dongtai.utils import const
from django.utils.translation import gettext_lazy as _

from iast.base.project_version import get_project_version


class ProjectDetail(UserEndPoint):
    name = "api-v1-project-<id>"
    description = _("View item details")

    def get(self, request, id):
        auth_users = self.get_auth_users(request.user)
        project = IastProject.objects.filter(user__in=auth_users, id=id).first()

        if project:
            relations = IastAgent.objects.filter(bind_project_id=project.id, online=const.RUNNING)
            agents = [{"id": relation.id, "name": relation.token} for relation in relations]
            if project.scan:
                scan_id = project.scan.id
            else:
                scan_id = 0
            
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
            return R.failure(status=203, msg=_('no permission'))
