######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : messages_send
# @created     : 星期四 10月 14, 2021 16:11:22 CST
#
# @description :
######################################################################


from dongtai_common.utils import const
from dongtai_common.models.message import IastMessage
from dongtai_common.endpoint import R
from dongtai_common.utils import const
from dongtai_common.endpoint import TalentAdminEndPoint
from django.forms.models import model_to_dict
from django.db.models import Q
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer
from django.utils.translation import gettext_lazy as _


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = IastMessage
        fields = [
            "id",
            "message",
            "relative_url",
            "create_time",
            "read_time",
            "is_read",
            "message_type_id",
            "to_user_id",
        ]


class MessagesSendEndpoint(TalentAdminEndPoint):
    @extend_schema_with_envcheck(
        request=MessageSerializer,
        summary=_("Send Message"),
        description=_("Used to get the message list corresponding to the user"),
        tags=[_("Messages")],
    )
    def post(self, request):
        ser = MessageSerializer(data=request.data)
        try:
            if ser.is_valid(True):
                pass
        except ValidationError as e:
            return R.failure(data=e.detail)
        IastMessage.create(**ser.validated_data)
        return R.success()
