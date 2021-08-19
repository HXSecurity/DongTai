#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:sjh
# software: PyCharm
# project: lingzhi-webapi
import logging, time
from dongtai.endpoint import R
from dongtai.endpoint import UserEndPoint
from dongtai.models.project_version import IastProjectVersion
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger("django")


class ProjectVersionList(UserEndPoint):
    name = "api-v1-project-version-list"
    description = _("View application version list")

    def get(self, request, project_id):
        try:
            auth_users = self.get_auth_users(request.user)
            versionInfo = IastProjectVersion.objects.filter(project_id=project_id, user__in=auth_users, status=1).order_by("-id")
            data = []
            if versionInfo:
                for item in versionInfo:
                    data.append({
                        "version_id": item.id,
                        "version_name": item.version_name,
                        "current_version": item.current_version,
                        "description": item.description,
                    })
            return R.success(msg=_('Search successful'), data=data)
        except Exception as e:
            return R.failure(status=202, msg=e)
