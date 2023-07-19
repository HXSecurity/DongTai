######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : messages_new
# @created     : 星期三 10月 13, 2021 15:30:46 CST
#
# @description :
######################################################################


from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.message import IastMessage
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer


class ResponseDataSerializer(serializers.Serializer):
    new_message_count = serializers.IntegerField(
        help_text=_("total number of new messages")
    )


_SuccessSerializer = get_response_serializer(ResponseDataSerializer())


class MessagesNewEndpoint(UserEndPoint):
    @extend_schema_with_envcheck(
        response_schema=_SuccessSerializer,
        summary=_("Messages Count"),
        description=_("Used to get the number of messages corresponding to the user"),
        tags=[_("Messages")],
    )
    def get(self, request):
        return R.success(
            data={
                "new_message_count": IastMessage.objects.filter(
                    to_user_id=request.user.id,
                ).count()
            },
        )
