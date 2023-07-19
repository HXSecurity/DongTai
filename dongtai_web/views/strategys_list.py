#!/usr/bin/env python

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.strategy_user import IastStrategyUser
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer


class _StrategyResponseDataStrategySerializer(serializers.Serializer):
    id = serializers.CharField(help_text=_("The id of agent"))
    name = serializers.CharField(help_text=_("The name of the strategy"))


_ResponseSerializer = get_response_serializer(
    data_serializer=_StrategyResponseDataStrategySerializer(many=True),
)


class StrategyList(UserEndPoint):
    @extend_schema_with_envcheck(
        tags=[_("Strategy")],
        summary=_("Strategy List (with user)"),
        description=_("Get a list of strategies."),
        response_schema=_ResponseSerializer,
    )
    def get(self, request):
        queryset = (
            IastStrategyUser.objects.filter(status=1)
            .values("id", "name")
            .order_by("-id")
        )
        data = []
        if queryset:
            for item in queryset:
                data.append(
                    {
                        "id": item["id"],
                        "name": item["name"],
                    }
                )
        return R.success(data=data)
