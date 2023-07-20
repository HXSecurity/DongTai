######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : messages_list
# @created     : 星期三 10月 13, 2021 14:34:14 CST
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
from dongtai_common.utils import const
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer


class _MessagesArgsSerializer(serializers.Serializer):
    page_size = serializers.IntegerField(default=20, help_text=_("Number per page"))
    page = serializers.IntegerField(default=1, help_text=_("Page index"))


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
            "message_type",
        ]


class PageSerializer(serializers.Serializer):
    alltotal = serializers.IntegerField(help_text=_("total_number"))
    num_pages = serializers.IntegerField(help_text=_("the number of pages"))
    page_size = serializers.IntegerField(help_text=_("Number per page"))


class ResponseDataSerializer(serializers.Serializer):
    messages = MessageSerializer(many=True)


_SuccessSerializer = get_response_serializer(ResponseDataSerializer())


class MessagesEndpoint(UserEndPoint):
    @extend_schema_with_envcheck(
        [_MessagesArgsSerializer],
        response_schema=_SuccessSerializer,
        summary=_("Get Messages List"),
        description=_("Used to get the message list corresponding to the user"),
        tags=[_("Messages")],
    )
    def get(self, request):
        ser = _MessagesArgsSerializer(data=request.GET)
        try:
            if ser.is_valid(True):
                page_size = ser.validated_data["page_size"]
                page = ser.validated_data["page"]
        except ValidationError as e:
            return R.failure(data=e.detail)
        queryset = (
            IastMessage.objects.filter(to_user_id=request.user.id)
            .order_by("-create_time")
            .all()
        )
        page_summary, messages = self.get_paginator(queryset, page, page_size)
        messages_data = MessageSerializer(messages, many=True).data
        for message in messages:
            message.is_read = 1
            message.save(update_fields=["is_read"])
        return R.success(
            data={"messages": messages_data, "page": page_summary},
        )
