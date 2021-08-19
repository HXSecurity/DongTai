#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi
import logging
import time

from django.db.models import Q

from dongtai.endpoint import R
from dongtai.endpoint import UserEndPoint
from dongtai.models.agent import IastAgent
from dongtai.models.project_version import IastProjectVersion
from dongtai.models.project import IastProject
from dongtai.models.strategy_user import IastStrategyUser
from iast.base.project_version import version_modify
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger("django")


class ProjectAdd(UserEndPoint):
    name = "api-v1-project-add"
    description = _("New application")

    def post(self, request):
        try:
            name = request.data.get("name")
            mode = request.data.get("mode")
            scan_id = request.data.get("scan_id")

            if not scan_id or not name or not mode:
                return R.failure(status=202, msg=_('Parameter error'))
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
                
                project = IastProject.objects.filter(id=pid, user=request.user).first()
                project.name = name
            else:
                
                project = IastProject.objects.filter(name=name, user=request.user).first()
                if not project:
                    project = IastProject.objects.create(name=name, user=request.user)
                else:
                    return R.failure(status=203, msg=_('Failed to create, the application name already exists'))
            versionInfo = IastProjectVersion.objects.filter(project_id=project.id, user=request.user, current_version=1, status=1).first()
            if versionInfo:
                project_version_id = versionInfo.id
            else:
                project_version_id =0
            current_project_version = {
                "project_id": project.id,
                "version_id": project_version_id,
                "version_name": version_name,
                "description": request.data.get("description", ""),
                "current_version": 1
            }
            result = version_modify(request.user, current_project_version)
            if result.get("status", "202") == "202":
                return R.failure(status=202, msg=_("Parameter error"))
            else:
                project_version_id = result.get("data", {}).get("version_id", 0)
            
            if agent_ids:
                haveBind = IastAgent.objects.filter(
                    ~Q(bind_project_id=project.id),
                    id__in=agents,
                    bind_project_id__gt=0,
                    user__in=auth_users).exists()
                if haveBind:
                    return R.failure(status=202, msg=_('Agent has been bound by other application'))

            project.scan = scan
            project.mode = mode
            project.agent_count = len(agents)
            project.user = request.user
            project.latest_time = int(time.time())
            
            if agents:
                IastAgent.objects.filter(user__in=auth_users, bind_project_id=project.id).update(bind_project_id=0, online=0)
                project.agent_count = IastAgent.objects.filter(
                    Q(id__in=agents) | Q(project_name=name),
                    user__in=auth_users,
                    bind_project_id=0,
                    project_version_id=0
                ).update(bind_project_id=project.id, project_version_id=project_version_id, online=1)
            else:
                project.agent_count = IastAgent.objects.filter(
                    user__in=auth_users,
                    bind_project_id=project.id
                ).update(bind_project_id=0, online=0)
                project.agent_count = IastAgent.objects.filter(
                    project_name=name, user__in=auth_users).update(
                        bind_project_id=project.id,
                        project_version_id=project_version_id)
            project.save(update_fields=['scan_id', 'mode', 'agent_count', 'user_id', 'latest_time'])

            return R.success(msg=_('Created success'))
        except Exception as e:
            print(e)
            return R.failure(status=202, msg=e)
