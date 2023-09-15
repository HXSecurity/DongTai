#!/usr/bin/env python
import logging

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.project_version import IastProjectVersion
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer

logger = logging.getLogger("django")


class _VersionListDataSerializer(serializers.ModelSerializer):
    version_id = serializers.IntegerField(source="IastProjectVersion.id", help_text=_("The version id of the project"))
    version_name = serializers.CharField(help_text=_("The version name of the project"))
    description = serializers.CharField(help_text=_("Description of the project versoin"))
    current_version = serializers.IntegerField(
        help_text=_("Whether it is the current version, 1 means yes, 0 means no.")
    )

    class Meta:
        model = IastProjectVersion
        fields = ["version_id", "version_name", "current_version", "description"]


_ProjectVersionListResponseSerializer = get_response_serializer(_VersionListDataSerializer(many=True))


class ProjectVersionList(UserEndPoint):
    name = "api-v1-project-version-list"
    description = _("View application version list")

    @extend_schema_with_envcheck(
        tags=[_("Project"), "集成"],
        summary=_("Projects Version List"),
        description=_("Get the version information list of the item corresponding to the id"),
        response_schema=_ProjectVersionListResponseSerializer,
    )
    def get(self, request, project_id):
        try:
            project = request.user.get_projects().filter(id=project_id).first()
            if not project:
                return R.failure(status=203, msg=_("no permission"))

            versionInfo = IastProjectVersion.objects.filter(project_id=project_id, status=1).order_by("-id")
            data = []
            if versionInfo:
                data = [
                    {
                        "version_id": item.id,
                        "version_name": item.version_name,
                        "current_version": item.current_version,
                        "description": item.description,
                    }
                    for item in versionInfo
                ]

            return R.success(msg=_("Search successful"), data=data)
        except Exception as e:
            logger.exception("uncatched exception: ", exc_info=e)
            return R.failure(status=202, msg=_("Parameter error"))
