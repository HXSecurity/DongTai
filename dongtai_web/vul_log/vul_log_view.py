from django.db.models import Q
from django.forms.models import model_to_dict
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, viewsets
from rest_framework.serializers import ValidationError

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.iast_vul_log import IastVulLog
from dongtai_web.common import VulType


class VulLogListArgsSerializer(serializers.Serializer):
    vul_type = serializers.IntegerField(min_value=1, max_value=2, help_text="漏洞类型")
    msg_type = serializers.IntegerField(min_value=1, max_value=5, required=False, help_text="消息类型")
    start_time = serializers.IntegerField(required=False, help_text="开始时间")
    end_time = serializers.IntegerField(required=False, help_text="结束时间")


class VulLogViewSet(UserEndPoint, viewsets.ViewSet):
    name = "api-v1-vul-log"
    description = _("vul-log")

    @extend_schema(
        parameters=[VulLogListArgsSerializer],
        tags=[_("Vulnerability")],
        summary="漏洞日志",
    )
    def list(self, request, vul_id):
        data = []
        ser = VulLogListArgsSerializer(data=request.GET)
        try:
            if ser.is_valid(True):
                pass
        except ValidationError as e:
            return R.failure(data=e.detail)
        auth_users = self.get_auth_users(request.user)
        vul_type = VulType(int(request.query_params.get("vul_type", 1)))
        msg_type = int(request.query_params.get("msg_type", 1))
        q = Q(user__in=auth_users)
        if vul_type == VulType.APPLICATION:
            q = q & Q(vul_id=vul_id)
        if vul_type == VulType.ASSET:
            q = q & Q(asset_vul_id=vul_id)
        if "msg_type" in request.query_params and msg_type:
            q = q & Q(msg_type=msg_type)
        if "start_time" in request.query_params and "end_time" in request.query_params:
            q = q & Q(datetime__gt=request.query_params["start_time"], datetime__lt=request.query_params["end_time"])
        data = IastVulLog.objects.filter(q).all()

        return R.success([model_to_dict(i) for i in data])
