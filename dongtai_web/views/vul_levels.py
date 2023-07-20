######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : vul_levels
# @created     : 星期五 11月 19, 2021 14:35:44 CST
#
# @description :
######################################################################


from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from dongtai_common.endpoint import AnonymousAndUserEndPoint, R
from dongtai_common.models.vul_level import IastVulLevel
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer


class IastVulLevelSerializers(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "name_value"]
        model = IastVulLevel


_ResponseSerializer = get_response_serializer(
    data_serializer=IastVulLevelSerializers(many=True),
)


class VulLevelList(AnonymousAndUserEndPoint):
    @extend_schema_with_envcheck(
        tags=[_("Vul level list")],
        summary=_("Vul level List"),
        description=_("Get a list of vul level."),
        response_schema=_ResponseSerializer,
    )
    def get(self, request):
        queryset = IastVulLevel.objects.all()
        return R.success(data=IastVulLevelSerializers(queryset, many=True).data)
