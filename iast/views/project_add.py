#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/27 上午10:52
# software: PyCharm
# project: lingzhi-webapi
import logging
import time

from django.db.models import Q

from base import R
from iast.base.user import UserEndPoint
from iast.models.agent import IastAgent
from iast.models.project import IastProject
from iast.models.strategy_user import IastStrategyUser

logger = logging.getLogger("django")


class ProjectAdd(UserEndPoint):
    """
    创建用户，默认只能创建普通用户
    """
    name = "api-v1-project-add"
    description = "新增项目"

    def post(self, request):
        try:
            name = request.data.get("name", None)
            mode = request.data.get("mode", None)
            # 扫描策略
            scan_id = request.data.get("scan_id", None)
            if not scan_id or not name or not mode:
                return R.failure(status=202, msg='参数错误')
            scan = IastStrategyUser.objects.filter(id=scan_id, user=request.user).first()
            agent_ids = request.data.get("agent_ids", None)
            if agent_ids:
                agents = agent_ids.split(',')
            else:
                agents = []

            pid = request.data.get("pid")
            auth_users = self.get_auth_users(request.user)
            if pid:
                project = IastProject.objects.filter(id=pid, user=request.user).first()
                project.name = name
            else:
                # 检测项目名称是否存在
                project = IastProject.objects.filter(name=name, user=request.user).first()
                if not project:
                    # 检测agent是否绑定其他项目
                    haveBind = IastAgent.objects.filter(
                        id__in=agents,
                        user__in=auth_users,
                        bind_project_id__gt=0
                    ).exists()
                    if haveBind:
                        return R.failure(status=202, msg='agent已被其他项目绑定')
                    project = IastProject.objects.create(name=name, user=request.user)

            # 检测agent是否绑定其他项目
            haveBind = IastAgent.objects.filter(
                ~Q(bind_project_id=project.id),
                id__in=agents,
                bind_project_id__gt=0,
                user__in=auth_users).exists()
            if haveBind:
                return R.failure(status=202, msg='agent已被其他项目绑定')
            project.scan = scan
            project.mode = mode
            project.agent_count = len(agents)
            project.user = request.user
            project.latest_time = int(time.time())
            # 创建项目-ID列表
            if agents:
                IastAgent.objects.filter(user__in=auth_users, bind_project_id=project.id).update(bind_project_id=0)
                project.agent_count = IastAgent.objects.filter(
                    user__in=auth_users,
                    id__in=agents,
                    bind_project_id=0
                ).update(bind_project_id=project.id)

            else:
                project.agent_count = IastAgent.objects.filter(
                    user__in=auth_users,
                    bind_project_id=project.id
                ).update(bind_project_id=0)
            project.save()

            return R.success(msg='创建成功')
        except Exception as e:
            return R.failure(status=202, msg=e)
