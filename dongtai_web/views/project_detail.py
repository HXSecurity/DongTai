#!/usr/bin/env python

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.agent import IastAgent
from dongtai_common.utils import const
from dongtai_web.base.project_version import (
    ProjectsVersionDataSerializer,
    get_project_version,
)
from dongtai_web.serializers.project import ProjectSerializer
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer


class ProjectsResponseDataSerializer(serializers.Serializer):
    name = serializers.CharField(help_text=_("The name of project"))
    agent_ids = serializers.CharField(help_text=_("The id corresponding to the agent, use, for segmentation."))
    mode = serializers.ChoiceField(["插桩模式"], help_text=_("The mode of project"))
    scan_id = serializers.IntegerField(help_text=_("The id corresponding to the scanning strategy."))
    versionData = ProjectsVersionDataSerializer(help_text=_("Version information about the project"))
    id = serializers.IntegerField(help_text=_("The id of the project"))
    vul_validation = serializers.IntegerField(help_text="vul validation switch")


_ResponseSerializer = get_response_serializer(
    ProjectsResponseDataSerializer(help_text=""),
    status_msg_keypair=(
        ((201, _("success")), ""),
        ((203, _("no permission")), ""),
    ),
)


class ProjectDetail(UserEndPoint):
    name = "api-v1-project-<id>"
    description = _("View item details")

    @extend_schema_with_envcheck(
        tags=[_("Project")],
        summary=_("Projects Detail"),
        description=_(
            "Get project information by project id, including the current version information of the project."
        ),
        response_schema=_ResponseSerializer,
    )
    def get(self, request, id):
        project = request.user.get_projects().filter(id=id).first()

        if project:
            relations = IastAgent.objects.filter(bind_project_id=project.id, online=const.RUNNING)
            agents = [{"id": relation.id, "name": relation.token} for relation in relations]
            if project.scan:
                scan_id = project.scan.id
                scan_name = project.scan.name
            else:
                scan_id = 0
                scan_name = ""

            current_project_version = get_project_version(project.id)
            return R.success(
                data={
                    "name": project.name,
                    "id": project.id,
                    "mode": project.mode,
                    "scan_id": scan_id,
                    "scan_name": scan_name,
                    "agents": agents,
                    "versionData": current_project_version,
                    "vul_validation": project.vul_validation,
                    "base_url": project.base_url,
                    "test_req_header_key": project.test_req_header_key,
                    "test_req_header_value": project.test_req_header_value,
                    "department_id": project.department.id,
                    "template_id": project.template_id,
                    "enable_log": project.enable_log,
                    "log_level": project.log_level,
                    "project_group_name": ProjectSerializer().get_project_group_name(project),
                }
            )
        return R.failure(status=203, msg=_("no permission"))
