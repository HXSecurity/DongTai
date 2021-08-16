#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi

from dongtai.endpoint import R
from dongtai.endpoint import UserEndPoint
from dongtai.models.agent import IastAgent
from dongtai.models.project import IastProject
from django.utils.translation import gettext_lazy as _


class ProjectDel(UserEndPoint):
    name = "api-v1-project-del"
    description = _("Delete project")

    def post(self, request):
        try:
            project_id = request.data['id']
            if project_id:
                auth_users = self.get_auth_users(request.user)
                IastAgent.objects.filter(bind_project_id=project_id, user__in=auth_users).update(bind_project_id=0)
                IastProject.objects.filter(id=project_id, user__in=auth_users).delete()

            return R.success(msg=_('Project deletion success'))
        except Exception as e:
            return R.failure(msg=e)
