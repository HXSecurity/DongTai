#!/usr/bin/env python

# status
import logging

from django.utils.translation import gettext_lazy as _

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.vulnerablity import IastVulnerabilityModel, IastVulnerabilityStatus
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer
from dongtai_web.vul_log.vul_log import log_change_status

logger = logging.getLogger("dongtai-webapi")

_ResponseSerializer = get_response_serializer(
    status_msg_keypair=(
        ((201, _("Vulnerability status is modified to {}")), ""),
        ((202, _("Incorrect parameter")), ""),
    )
)


class VulStatus(UserEndPoint):
    name = "api-v1-vuln-status"
    description = _("Modify the vulnerability status")

    @extend_schema_with_envcheck(
        [],
        [
            {
                "name": _("Update with status_id"),
                "description": _("Update vulnerability status with status id."),
                "value": {"id": 1, "status_id": 1},
            },
            {
                "name": _("Update with status name(Not recommended)"),
                "description": _("Update vulnerability status with status name."),
                "value": {"id": 1, "status": "str"},
            },
        ],
        [
            {
                "name": _("Get data sample"),
                "description": _(
                    "The aggregation results are programming language, risk level, vulnerability type, project"
                ),
                "value": {
                    "status": 201,
                    "msg": "Vulnerability status is modified to Confirmed",
                },
            }
        ],
        tags=[_("Vulnerability")],
        summary=_("Vulnerability Status Modify"),
        description=_(
            """Modify the vulnerability status of the specified id.
        The status is specified by the following two parameters.
        Status corresponds to the status noun and status_id corresponds to the status id.
        Both can be obtained from the vulnerability status list API, and status_id is preferred."""
        ),
        response_schema=_ResponseSerializer,
    )
    def post(self, request):
        vul_id = request.data.get("vul_id")
        vul_ids = request.data.get("vul_ids")
        status_id = request.data.get("status_id")
        user = request.user
        user_id = user.id
        department = request.user.get_relative_department()
        if not (isinstance(vul_id, int) or isinstance(vul_ids, list)):
            return R.failure()
        if not vul_ids:
            vul_ids = [vul_id]
        queryset = IastVulnerabilityModel.objects.filter(
            is_del=0, project__department__in=department
        )
        vul_status = IastVulnerabilityStatus.objects.filter(pk=status_id).first()
        if vul_status:
            queryset_status = queryset.filter(id__in=vul_ids)
            ids = []
            for vul in queryset_status:
                vul.status_id = status_id
                vul.save()
                ids.append(vul.id)

            #     queryset.filter(id__in=vul_ids).values_list('id', flat=True))
            log_change_status(user_id, request.user.username, ids, vul_status.name)
        return R.success()
