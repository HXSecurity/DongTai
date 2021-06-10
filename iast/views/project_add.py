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
from dongtai_models.models.project_version import IastProjectVersion
from dongtai_models.models.project import IastProject
from dongtai_models.models.strategy_user import IastStrategyUser
from iast.base.project_version import version_modify

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

            version_name = request.data.get("version_name", "")
            if not version_name:
                version_name = "V1.0"
            pid = request.data.get("pid", 0)

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
            versionData = {
                "project_id": project.id,
                "version_id": request.data.get("version_id", 0),
                "version_name": version_name,
                "description": request.data.get("description", ""),
                "current_version": 1
            }
            result = version_modify(request.user, versionData)
            if result.get("status", "202") == "202":
                return R.failure(status=202, msg=result.get("msg", "参数错误"))
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
            print(e)
            return R.failure(status=202, msg=e)
