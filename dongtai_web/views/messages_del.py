######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : messages_del
# @created     : 星期三 10月 13, 2021 15:47:31 CST
#
# @description :
######################################################################
from django.db.models import Q
from django.forms.models import model_to_dict
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.message import IastMessage
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer


class _MessagesDelArgsSerializer(serializers.Serializer):
    id = serializers.IntegerField(
        required=False, default=None, help_text=_("The id of Message")
    )
    all = serializers.NullBooleanField(
        required=False,
        default=False,
        help_text=_("delete all messages when all is True"),
    )


class MessagesDelEndpoint(UserEndPoint):
    @extend_schema_with_envcheck(
        request=_MessagesDelArgsSerializer,
        summary=_("Messages Delete"),
        description=_("Used by the user to delete the corresponding message"),
        tags=[_("Messages")],
    )
    def post(self, request):
        ser = _MessagesDelArgsSerializer(data=request.data)
        try:
            if ser.is_valid(True):
                id_ = ser.validated_data["id"]
                all_ = ser.validated_data["all"]
        except ValidationError as e:
            return R.failure(data=e.detail)
        if all_ is True:
            IastMessage.objects.filter(to_user_id=request.user.id).all().delete()
        else:
            IastMessage.objects.filter(to_user_id=request.user.id, pk=id_).delete()
        return R.success(msg="success")
