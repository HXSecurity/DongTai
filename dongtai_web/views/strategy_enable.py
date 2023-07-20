#!/usr/bin/env python

from dongtai_common.models.hook_type import HookType
from dongtai_common.models.hook_strategy import HookStrategy
from dongtai_common.utils import const
from dongtai_common.models.strategy import IastStrategyModel

from dongtai_common.endpoint import R
from dongtai_common.endpoint import TalentAdminEndPoint
from django.utils.translation import gettext_lazy as _
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer

_ResponseSerializer = get_response_serializer(
    status_msg_keypair=(
        ((201, _("Policy enabled success, total {} hook rules")), ""),
        ((202, _("Strategy does not exist")), ""),
    )
)

ENABLE = "enable"


class StrategyEnableEndpoint(TalentAdminEndPoint):
    @extend_schema_with_envcheck(
        tags=[_("Strategy")],
        summary=_("Strategy Enbale"),
        description=_("Enable the corresponding strategy according to id"),
        response_schema=_ResponseSerializer,
    )
    def get(self, request, id):
        strategy = IastStrategyModel.objects.filter(id=id).first()
        strategy_models = HookType.objects.filter(vul_strategy=strategy).all()
        if strategy:
            strategy.state = ENABLE
            strategy.save()
            total_counts = 0
            for strategy_model in strategy_models:
                counts = strategy_model.strategies.filter(
                    enable=const.HOOK_TYPE_DISABLE
                ).update(enable=const.HOOK_TYPE_ENABLE)
                strategy_model.enable = const.HOOK_TYPE_ENABLE
                strategy_model.save(update_fields=["enable"])
                total_counts += counts
            return R.success(
                msg=_("Policy enabled success, total {} hook rules").format(
                    total_counts
                )
            )
        else:
            return R.failure(msg=_("Strategy does not exist"))


if __name__ == "__main__":
    HookStrategy.objects.values("id").count()
