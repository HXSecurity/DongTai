from django.forms.models import model_to_dict
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.iast_vul_log import IastVulLog
from dongtai_web.common import VulType


class VulLogViewSet(UserEndPoint, viewsets.ViewSet):
    name = "api-v1-vul-log"
    description = _("vul-log")

    @extend_schema(
        tags=[_("Vulnerability")],
        summary="漏洞日志",
    )
    def list(self, request, vul_id):
        data = []
        auth_users = self.get_auth_users(request.user)
        vul_type = VulType(int(request.query_params.get("vul_type", 1)))
        if vul_type == VulType.APPLICATION:
            data = IastVulLog.objects.filter(vul_id=vul_id, user__in=auth_users).all()
        if vul_type == VulType.ASSET:
            data = IastVulLog.objects.filter(asset_vul_id=vul_id, user__in=auth_users).all()

        return R.success([model_to_dict(i) for i in data])
