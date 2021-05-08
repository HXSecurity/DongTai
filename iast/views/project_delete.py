#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/27 上午10:52
# software: PyCharm
# project: lingzhi-webapi

from base import R
from iast.base.user import UserEndPoint
from dongtai_models.models.agent import IastAgent
from dongtai_models.models.project import IastProject


class ProjectDel(UserEndPoint):
    """
    创建用户，默认只能创建普通用户
    """
    name = "api-v1-project-del"
    description = "删除项目"

    def post(self, request):
        try:
            project_id = request.data['id']
            if project_id:
                auth_users = self.get_auth_users(request.user)
                IastAgent.objects.filter(bind_project_id=project_id, user__in=auth_users).update(bind_project_id=0)
                IastProject.objects.filter(id=project_id, user__in=auth_users).delete()

            return R.success(msg='项目删除成功')
        except Exception as e:
            return R.failure(msg=e)
