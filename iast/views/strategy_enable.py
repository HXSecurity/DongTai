#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad

# software: PyCharm
# project: lingzhi-webapi
from dongtai.models.hook_type import HookType
from dongtai.models.hook_strategy import HookStrategy
from dongtai.utils import const

from dongtai.endpoint import R
from dongtai.endpoint import TalentAdminEndPoint
from django.utils.translation import gettext_lazy as _
from iast.utils import extend_schema_with_envcheck, get_response_serializer

_ResponseSerializer = get_response_serializer(status_msg_keypair=(
    ((201, _('Policy enabled success, total {} hook rules')), ''),
    ((202, _('Strategy does not exist')), ''),
))


class StrategyEnableEndpoint(TalentAdminEndPoint):
    @extend_schema_with_envcheck(
        tags=[_('Strategy')],
        summary=_('Strategy Enbale'),
        description=_(
            "Enable the corresponding strategy according to id"
        ),
        response_schema=_ResponseSerializer,
    )
    def get(self, request, id):
        strategy_model = HookType.objects.filter(id=id).first()
        if strategy_model:
            counts = strategy_model.strategies.filter(enable=const.HOOK_TYPE_DISABLE).update(
                enable=const.HOOK_TYPE_ENABLE)
            strategy_model.enable = const.HOOK_TYPE_ENABLE
            strategy_model.save(update_fields=['enable'])

            return R.success(msg=_('Policy enabled success, total {} hook rules').format(counts))
        else:
            return R.failure(msg=_('Strategy does not exist'))


if __name__ == '__main__':
    
    HookStrategy.objects.values("id").count()
