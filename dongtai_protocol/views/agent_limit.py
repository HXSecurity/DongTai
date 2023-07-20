import logging

from django.forms.models import model_to_dict
from drf_spectacular.utils import extend_schema

from dongtai_common.endpoint import OpenApiEndPoint, R
from dongtai_common.models.profile import IastProfile

logger = logging.getLogger("dongtai.openapi")


class LimitView(OpenApiEndPoint):
    @extend_schema(summary="agent限制", tags=["Agent服务端交互协议"], deprecated=True, methods=["GET"])
    def get(self, request):
        keys = ["cpu_limit"]
        profiles = IastProfile.objects.filter(key__in=keys).all()
        if profiles:
            data = [model_to_dict(profile) for profile in profiles]
        else:
            data = [{"id": 1, "key": "cpu_limit", "value": "60"}]
        return R.success(data=data)
