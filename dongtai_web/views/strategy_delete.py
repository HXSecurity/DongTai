#!/usr/bin/env python
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from dongtai_common.endpoint import R, TalentAdminEndPoint
from dongtai_common.models.hook_type import HookType
from dongtai_common.models.strategy import IastStrategyModel
from dongtai_common.utils import const
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer


class _StrategyResponseDataStrategySerializer(serializers.Serializer):
    id = serializers.CharField(help_text=_("The id of strategy"))


_ResponseSerializer = get_response_serializer(
    data_serializer=_StrategyResponseDataStrategySerializer(many=True),
)

DELETE = "delete"


class StrategyDelete(TalentAdminEndPoint):
    @extend_schema_with_envcheck(
        tags=[_("Strategy")],
        summary=_("Strategy Delete"),
        description=_("Delete the corresponding strategy according to id"),
        response_schema=_ResponseSerializer,
    )
    def delete(self, request, id_: int):
        if id_ <= 0:
            return R.failure()
        strategy = IastStrategyModel.objects.filter(pk=id_).first()
        if not strategy:
            return R.failure(msg=_("This strategy does not exist"))
        if strategy.system_type == 1:
            return R.failure(msg="Can not delete system strategy")
        hook_types = HookType.objects.filter(vul_strategy=strategy).all()
        strategy.state = DELETE
        strategy.save()
        for hook_type in hook_types:
            # need to check why language_id show 0
            if hook_type.language_id == 0:
                continue
            hook_strategies = hook_type.strategies.all()
            for hook_strategy in hook_strategies:
                hook_strategy.enable = const.DELETE
                hook_strategy.save()
            hook_type.enable = const.DELETE
            hook_type.save()
        return R.success(data={"id": id_})
