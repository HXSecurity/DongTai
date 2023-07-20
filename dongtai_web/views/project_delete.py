#!/usr/bin/env python

import logging
from dongtai_common.endpoint import R
from dongtai_common.endpoint import UserEndPoint
from dongtai_common.models.agent import IastAgent
from dongtai_common.models.project import IastProject
from django.utils.translation import gettext_lazy as _
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer
from rest_framework import serializers


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
                department = request.user.get_relative_department()
                #                IastAgent.objects.filter(
                #                    user__in=auth_users).update(bind_project_id=-1)
                IastProject.objects.filter(
                    id=project_id, department__in=department
                ).delete()

            return R.success(msg=_("Application has been deleted successfully"))
        except Exception as e:
            logger.error(e, exc_info=e)
            return R.failure(msg=_("Failed to delete the project."))
