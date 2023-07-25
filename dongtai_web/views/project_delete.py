#!/usr/bin/env python

import logging

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer


class _ProjectsDelBodyArgsSerializer(serializers.Serializer):
    id = serializers.IntegerField(help_text=_("The id of the project"))


logger = logging.getLogger("django")
_ResponseSerializer = get_response_serializer(
    status_msg_keypair=(
        ((201, _("Application has been deleted successfully")), ""),
        ((202, _("Failed to delete the project.")), ""),
    )
)


class ProjectDel(UserEndPoint):
    name = "api-v1-project-del"
    description = _("Delete application")

    @extend_schema_with_envcheck(
        request=_ProjectsDelBodyArgsSerializer,
        tags=[_("Project")],
        summary=_("Projects Delete"),
        description=_("Delete the agent by specifying the id."),
        response_schema=_ResponseSerializer,
    )
    def post(self, request):
        try:
            project_id = request.data.get("id", None)
            if project_id:
                projects = request.user.get_projects()
                projects.filter(id=project_id).delete()

            return R.success(msg=_("Application has been deleted successfully"))
        except Exception as e:
            logger.exception("uncatched exception: ", exc_info=e)
            return R.failure(msg=_("Failed to delete the project."))
