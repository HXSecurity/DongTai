import logging

from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import serializers

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.agent_method_pool import VulMethodPool
from dongtai_common.utils.request_type import Request

logger = logging.getLogger("dongtai-webapi")


class VulMethodPoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = VulMethodPool
        fields = [
            "method_pool_id",
            "vul_id",
            "agent_id",
            "url",
            "uri",
            "http_method",
            "http_scheme",
            "http_protocol",
            "req_header",
            "req_params",
            "req_data",
            "res_header",
            "res_body",
            "req_header_fs",
            "context_path",
            "method_pool",
            "pool_sign",
            "clent_ip",
            "create_time",
            "update_time",
            "uri_sha1",
        ]


class VulMethodPoolDownload(UserEndPoint):
    @extend_schema(
        summary=_("Vulnerability Method Pool Download"),
        tags=[_("Vulnerability")],
        description=_("Get the raw method pool of the corresponding vulnerability by specifying the id"),
    )
    def get(self, request: Request, id: int):
        try:
            return R.success(
                data=VulMethodPoolSerializer(
                    VulMethodPool.objects.filter(vul_id=id).order_by("-update_time").first()
                ).data
            )
        except Exception as e:
            logger.exception("operation failed", exc_info=e)
            return R.failure(data="operation failed")
