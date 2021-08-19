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


class ProjectVersionDelete(UserEndPoint):
    name = "api-v1-project-version-delete"
    description = _("Delete application version information")

    def post(self, request):
        try:
            version_id = request.data.get("version_id", 0)
            project_id = request.data.get("project_id", 0)
            if not version_id or not project_id:
                return R.failure(status=202, msg=_('Parameter error'))
            version = IastProjectVersion.objects.filter(id=version_id, project_id=project_id, user=request.user, status=1).first()
            if version:
                version.status = 0
                version.update_time = int(time.time())
                version.save(update_fields=['status'])
                return R.success(msg=_('Deleted Successfully'))
            else:
                return R.failure(status=202, msg=_('Version does not exist'))

        except Exception as e:
            return R.failure(status=202, msg=e)
