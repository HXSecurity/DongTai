#!/usr/bin/env python

# status
import logging

from django.utils.translation import gettext_lazy as _

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.vulnerablity import (
    IastVulnerabilityModel,
    IastVulnerabilityStatus,
)
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer
from dongtai_web.vul_log.vul_log import log_change_status
from rest_framework import serializers


logger = logging.getLogger("dongtai-webapi")

_ResponseSerializer = get_response_serializer(
    status_msg_keypair=(
        ((201, _("Vulnerability status is modified to {}")), ""),
        ((202, _("Incorrect parameter")), ""),
    )
)


class VulStatusChangeArgsSerializer(serializers.Serializer):
    vul_id = serializers.IntegerField(help_text=_("Vul id"), required=False)
    vul_ids = serializers.ListField(
        required=False, child=serializers.IntegerField(), default=[], help_text=_("Page index")
    )
    status_id = serializers.IntegerField(required=True, help_text=_("Document's corresponding programming language"))
    addtional_msg = serializers.CharField(default=None, help_text=_("Document's corresponding programming language"))


class VulStatus(UserEndPoint):
    name = "api-v1-vuln-status"
    description = _("Modify the vulnerability status")

    @extend_schema_with_envcheck(
        tags=[_("Vulnerability")],
        summary=_("Vulnerability Status Modify"),
        description=_(
            """Modify the vulnerability status of the specified id.
        The status is specified by the following two parameters.
        Status corresponds to the status noun and status_id corresponds to the status id.
        Both can be obtained from the vulnerability status list API, and status_id is preferred."""
        ),
        response_schema=_ResponseSerializer,
        request=VulStatusChangeArgsSerializer,
    )
    def post(self, request):
        vul_id = request.data.get("vul_id")
        vul_ids = request.data.get("vul_ids")
        status_id = request.data.get("status_id")
        addtional_msg = request.data.get("addtional_msg", "")

        user = request.user
        user_id = user.id
        projects = request.user.get_projects()
        if not (isinstance(vul_id, int) or isinstance(vul_ids, list)):
            return R.failure()
        if not vul_ids:
            vul_ids = [vul_id]
        queryset = IastVulnerabilityModel.objects.filter(is_del=0, project__in=projects)
        vul_status = IastVulnerabilityStatus.objects.filter(pk=status_id).first()
        if vul_status:
            queryset_status = queryset.filter(id__in=vul_ids)
            ids = []
            for vul in queryset_status:
                vul.status_id = status_id
                vul.save()
                ids.append(vul.id)

            #     queryset.filter(id__in=vul_ids).values_list('id', flat=True))
            log_change_status(user_id, request.user.username, ids, vul_status.name, addtional_msg)
        return R.success()
