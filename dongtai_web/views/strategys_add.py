#!/usr/bin/env python

from rest_framework.request import Request

from dongtai_common.endpoint import R
from dongtai_common.endpoint import UserEndPoint
from dongtai_common.models.strategy_user import IastStrategyUser
from django.utils.translation import gettext_lazy as _
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer

from rest_framework import serializers


class _StrategyResponseDataStrategySerializer(serializers.Serializer):
    id = serializers.CharField(help_text=_("The id of strategy"))


class _StrategyAddBodyargsSerializer(serializers.Serializer):
    ids = serializers.CharField(
        help_text=_('The id corresponding to the strategys, use"," for segmentation.')
    )
    name = serializers.CharField(help_text=_("The name of strategy"))


_ResponseSerializer = get_response_serializer(
    data_serializer=_StrategyResponseDataStrategySerializer(many=True),
)


class StrategyAdd(UserEndPoint):
    @extend_schema_with_envcheck(
        request=_StrategyAddBodyargsSerializer,
        tags=[_("Strategy")],
        summary=_("Sacn Strategy Add"),
        description=_(
            "Generate corresponding strategy group according to the strategy selected by the user."
        ),
        response_schema=_ResponseSerializer,
    )
    def post(self, request):
        ids = request.data.get("ids", None)

        name = request.data.get("name", None)
        user = request.user
        if not ids or not name:
            return R.failure(msg=_("Parameter error"))
        new_strategy = IastStrategyUser.objects.create(
            name=name, content=ids, user=user, status=1
        )
        return R.success(data={"id": new_strategy.id})
