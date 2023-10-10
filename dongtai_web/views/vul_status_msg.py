#!/usr/bin/env python

# status
import logging

from django.utils.translation import gettext_lazy as _

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.iast_vul_log import IastVulLog, MessageTypeChoices
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer

logger = logging.getLogger("dongtai-webapi")

_ResponseSerializer = get_response_serializer(
    status_msg_keypair=(
        ((201, _("Vulnerability status is modified to {}")), ""),
        ((202, _("Incorrect parameter")), ""),
    )
)


class VulStatusMsg(UserEndPoint):
    name = "api-v1-vuln-status"
    description = _("Modify the vulnerability status")

    @extend_schema_with_envcheck(
        tags=[_("Vulnerability")],
        summary="漏洞的最新评论",
        response_schema=_ResponseSerializer,
    )
    def get(self, request, vul_id):
        latest_log_msg = IastVulLog.objects.filter(vul_id=vul_id, msg_type=MessageTypeChoices.CHANGE_STATUS).last()
        if not latest_log_msg or "addtional_msg" not in latest_log_msg.meta_data:
            return R.success(data="")
        return R.success(data=latest_log_msg.meta_data["addtional_msg"])
