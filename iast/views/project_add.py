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
from dongtai_models.models.agent import IastAgent
from dongtai_models.models.project import IastProject
from dongtai_models.models.strategy_user import IastStrategyUser

logger = logging.getLogger("django")


class ProjectAdd(UserEndPoint):
    """
    创建用户，默认只能创建普通用户
    """
    name = "api-v1-project-add"
    description = "新增项目"

    def post(self, request):
        try:
            name = request.data.get("name")
            mode = request.data.get("mode")
            scan_id = request.data.get("scan_id")
            if not scan_id or not name or not mode:
                return R.failure(status=202, msg='参数错误')

            auth_users = self.get_auth_users(request.user)

            scan = IastStrategyUser.objects.filter(id=scan_id, user=request.user).first()
            agent_ids = request.data.get("agent_ids", None)
            if agent_ids:
                agents = agent_ids.split(',')
            else:
                agents = []

            pid = request.data.get("pid")
            if pid:
                # 如果存在pid，走修改逻辑
                project = IastProject.objects.filter(id=pid, user=request.user).first()
                project.name = name
            else:
                # 检测项目名称是否存在
                project = IastProject.objects.filter(name=name, user=request.user).first()
                if not project:
                    project = IastProject.objects.create(name=name, user=request.user)
                else:
                    return R.failure(status=203, msg='创建失败，项目名称已存在')

            # 检测agent是否绑定其他项目
            if agent_ids:
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
                    Q(id__in=agents) | Q(project_name=name),
                    user__in=auth_users,
                    bind_project_id=0
                ).update(bind_project_id=project.id)
            else:
                project.agent_count = IastAgent.objects.filter(
                    user__in=auth_users,
                    bind_project_id=project.id
                ).update(bind_project_id=0)
                project.agent_count = IastAgent.objects.filter(
                    project_name=name,
                    user__in=auth_users
                ).update(bind_project_id=project.id)
            project.save(update_fields=['scan_id', 'mode', 'agent_count', 'user_id', 'latest_time'])

            return R.success(msg='创建成功')
        except Exception as e:
            return R.failure(status=202, msg=e)
