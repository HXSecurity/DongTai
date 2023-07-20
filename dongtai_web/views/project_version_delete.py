#!/usr/bin/env python
import logging
import time

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.project_version import IastProjectVersion
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer

logger = logging.getLogger("django")


class _ProjectVersionDeleteSerializer(serializers.Serializer):
    version_id = serializers.CharField(help_text=_("The version id of the project"))
    project_id = serializers.IntegerField(help_text=_("The id of the project"))


_ResponseSerializer = get_response_serializer(
    status_msg_keypair=(
        ((202, _("Parameter error")), ""),
        ((201, _("Version does not exist")), ""),
        ((201, _("Deleted Successfully")), ""),
    )
)


class ProjectVersionDelete(UserEndPoint):
    name = "api-v1-project-version-delete"
    description = _("Delete application version information")

    @extend_schema_with_envcheck(
        request=_ProjectVersionDeleteSerializer,
        tags=[_("Project")],
        summary=_("Projects Version Delete"),
        description=_(
            "Delete the specified project version according to the conditions."
        ),
        response_schema=_ResponseSerializer,
    )
    def post(self, request):
        try:
            version_id = request.data.get("version_id", 0)
            project_id = request.data.get("project_id", 0)
            if not version_id or not project_id:
                return R.failure(status=202, msg=_("Parameter error"))
            version = IastProjectVersion.objects.filter(
                id=version_id, project_id=project_id, status=1
            ).first()
            if version:
                version.status = 0
                version.update_time = int(time.time())
                version.save(update_fields=["status"])
                return R.success(msg=_("Deleted Successfully"))
            return R.failure(status=202, msg=_("Version does not exist"))

        except Exception as e:
            logger.exception("uncatched exception: ", exc_info=e)
            return R.failure(status=202, msg=_("Parameter error"))
