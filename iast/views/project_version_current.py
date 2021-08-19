#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:sjh

# software: PyCharm
# project: lingzhi-webapi
import logging, time
from dongtai.endpoint import R
from django.db.models import Q
from dongtai.endpoint import UserEndPoint
from dongtai.models.project_version import IastProjectVersion
from dongtai.models.agent import IastAgent
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger("django")


class ProjectVersionCurrent(UserEndPoint):
    name = "api-v1-project-version-current"
    description = _("Set to the current application version")

    def post(self, request):
        try:
            project_id = request.data.get("project_id", 0)
            version_id = request.data.get("version_id", 0)
            if not version_id or not project_id:
                return R.failure(status=202, msg=_('Parameter error'))

            
            version = IastProjectVersion.objects.filter(project_id=project_id, id=version_id, user=request.user).first()
            if version:
                version.current_version = 1
                version.update_time = int(time.time())
                version.save(update_fields=["current_version", "update_time"])
                IastAgent.objects.filter(user=request.user, bind_project_id=project_id, project_version_id=version_id).update(online=1)
                
                IastAgent.objects.filter(~Q(project_version_id=version_id), user=request.user, bind_project_id=project_id).update(online=0)
                IastProjectVersion.objects.filter(
                    ~Q(id=version_id),
                    project_id=project_id,
                    user=request.user,
                    current_version=1,
                    status=1
                ).update(current_version=0, update_time=int(time.time()))

                return R.success(msg=_('Version setting success'))
            else:
                return R.failure(status=202, msg=_('Version does not exist'))

        except Exception as e:
            return R.failure(status=202, msg=_("Version setting failed"))
