######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : agent_alias_modified
# @created     : 星期三 10月 20, 2021 11:20:20 CST
#
# @description :
######################################################################

from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer
from dongtai_common.endpoint import UserEndPoint, R
from rest_framework import serializers
from dongtai_common.models.agent import IastAgent
from rest_framework.serializers import ValidationError
from django.utils.translation import gettext_lazy as _


class AgentAliasArgsSerializer(serializers.Serializer):
    id = serializers.IntegerField(help_text=_("The id corresponding to the agent."))
    alias = serializers.CharField(help_text=_("The alias corresponding to the agent."))


_ResponseSerializer = get_response_serializer(
    status_msg_keypair=(
        ((201, _("modified successfully")), ""),
        ((202, _("Agent does not exist or no permission to access")), ""),
        ((202, _("Error while deleting, please try again later")), ""),
    )
)


class AgentAliasModified(UserEndPoint):
    @extend_schema_with_envcheck(
        tags=[_("Agent")],
        request=AgentAliasArgsSerializer,
        summary=_("Agent Alias Modified"),
        description=_("Modified the agent alias"),
        response_schema=_ResponseSerializer,
    )
    def post(self, request):
        ser = AgentAliasArgsSerializer(data=request.data)
        try:
            if ser.is_valid(True):
                id_ = ser.validated_data["id"]
                alias = ser.validated_data["alias"]
        except ValidationError as e:
            return R.failure(data=e.detail)
        IastAgent.objects.filter(pk=id_).update(alias=alias)
        return R.success(msg=_("modified successfully"))
