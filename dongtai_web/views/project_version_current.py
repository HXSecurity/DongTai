#!/usr/bin/env python

import logging
import time

from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.project_version import IastProjectVersion
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer

logger = logging.getLogger("django")


class _ProjectVersionCurrentSerializer(serializers.Serializer):
    version_id = serializers.CharField(help_text=_("The version id of the project"))
    project_id = serializers.IntegerField(help_text=_("The id of the project"))


_ResponseSerializer = get_response_serializer(
    status_msg_keypair=(
        ((202, _("Version does not exist")), ""),
        ((202, _("Version setting failed")), ""),
        ((201, _("Version setting success")), ""),
    )
)


class ProjectVersionCurrent(UserEndPoint):
    name = "api-v1-project-version-current"
    description = _("Set to the current application version")

    @extend_schema_with_envcheck(
        request=_ProjectVersionCurrentSerializer,
        tags=[_("Project")],
        summary=_("Projects Version Current"),
        description=_(
            "Specify the selected version as the current version of the project according to the given conditions."
        ),
        response_schema=_ResponseSerializer,
    )
    def post(self, request):
        try:
            project_id = request.data.get("project_id", 0)
            version_id = request.data.get("version_id", 0)
            if not version_id or not project_id:
                return R.failure(status=202, msg=_("Parameter error"))

            projects = request.user.get_projects()
            version = IastProjectVersion.objects.filter(
                project_id=project_id, id=version_id, project__in=projects
            ).first()
            if version:
                version.current_version = 1
                version.update_time = int(time.time())
                version.save(update_fields=["current_version", "update_time"])
                IastProjectVersion.objects.filter(
                    ~Q(id=version_id),
                    project_id=project_id,
                    current_version=1,
                    status=1,
                ).update(current_version=0, update_time=int(time.time()))

                return R.success(msg=_("Version setting success"))
            return R.failure(status=202, msg=_("Version does not exist"))

        except Exception as e:
            logger.exception("uncatched exception: ", exc_info=e)
            return R.failure(status=202, msg=_("Version setting failed"))
