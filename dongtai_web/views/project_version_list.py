#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:sjh
# software: PyCharm
# project: lingzhi-webapi
import logging, time
from dongtai_common.endpoint import R
from dongtai_common.endpoint import UserEndPoint
from dongtai_common.models.project_version import IastProjectVersion
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer

logger = logging.getLogger("django")


class _VersionListDataSerializer(serializers.ModelSerializer):
    version_id = serializers.IntegerField(
        source='IastProjectVersion.id', help_text=_("The version id of the project"))
    version_name = serializers.CharField(
        help_text=_("The version name of the project"))
    description = serializers.CharField(
        help_text=_("Description of the project versoin"))
    current_version = serializers.IntegerField(help_text=_(
        "Whether it is the current version, 1 means yes, 0 means no."))

    class Meta:
        model = IastProjectVersion
        fields = ['version_id', 'version_name', 'current_version', 'description']

_ProjectVersionListResponseSerializer = get_response_serializer(
    _VersionListDataSerializer(many=True))

class ProjectVersionList(UserEndPoint):
    name = "api-v1-project-version-list"
    description = _("View application version list")

    @extend_schema_with_envcheck(
        tags=[_('Project')],
        summary=_('Projects Version List'),
        description=_("Get the version information list of the item corresponding to the id"),
        response_schema=_ProjectVersionListResponseSerializer,
    )
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
            logger.error(e)
            return R.failure(status=202, msg=_('Parameter error'))
