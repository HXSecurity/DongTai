import logging

from dongtai_common.models.hook_strategy import HookStrategy
from dongtai_common.models.hook_type import HookType
from drf_spectacular.utils import extend_schema
from rest_framework.request import Request
from dongtai_common.models.strategy import IastStrategyModel
from dongtai_common.utils import const
from dongtai_common.endpoint import OpenApiEndPoint, R
from django.db.models import (Prefetch, OuterRef, Subquery)
# note: 当前依赖必须保留，否则无法通过hooktype反向查找策略
from dongtai_protocol.api_schema import DongTaiParameter
from dongtai_protocol.views.hook_profiles import HookProfilesEndPoint, JAVA, convert_strategy
from django.db.models import Q

logger = logging.getLogger("django")


class HookProfilesV2EndPoint(HookProfilesEndPoint):
    name = "api-v1-profilesv2"
    description = "获取HOOK策略"

    @staticmethod
    def get_profiles(user=None, language_id=JAVA):
        profiles = list()
        hook_types_a = HookType.objects.filter(language_id=language_id,
                                               enable=const.HOOK_TYPE_ENABLE,
                                               type__in=(1, 2, 3))
        hook_types = IastStrategyModel.objects.filter(
            Q(state__in=['enable'],
              user_id__in=set([1, user.id]) if user else [1])).order_by('id')
        for hook_type in list(hook_types) + list(hook_types_a):
            strategy_details = list()
            if isinstance(hook_type, IastStrategyModel):
                hook_type = convert_strategy(hook_type)
            strategies = hook_type.strategies.filter(
                type__in=(1, 2, 3)
                if not isinstance(hook_type, IastStrategyModel) else [4],
                enable=const.HOOK_TYPE_ENABLE,
                language_id=language_id).values()
            for strategy in strategies:
                profiles.append({
                    'type': hook_type.type,
                    'vul_type': hook_type.value,
                    "source": strategy.get("source"),
                    "target": strategy.get("target"),
                    "signature": strategy.get("value"),
                    "inherit": strategy.get("inherit"),
                    "ignore_blacklist": strategy.get("ignore_blacklist"),
                    "ignore_internal": strategy.get("ignore_internal"),
                })
        return profiles
