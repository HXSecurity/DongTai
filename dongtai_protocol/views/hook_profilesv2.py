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
from dongtai_protocol.views.hook_profiles import HookProfilesEndPoint, JAVA

logger = logging.getLogger("django")


class HookProfilesV2EndPoint(HookProfilesEndPoint):
    name = "api-v1-profilesv2"
    description = "获取HOOK策略"

    @staticmethod
    def get_profiles(user=None, language_id=JAVA):
        profiles = list()
        hook_types = HookType.objects.filter(vul_strategy__state='enable',
                                             vul_strategy__user_id__in=set(
                                                 [1, user.id]),
                                             language_id=language_id,
                                             enable=const.HOOK_TYPE_ENABLE,
                                             type__in=(3, 4))
        hook_types_a = HookType.objects.filter(language_id=language_id,
                                               enable=const.HOOK_TYPE_ENABLE,
                                               type__in=(1, 2))
        for hook_type in list(hook_types) + list(hook_types_a):
            strategy_details = list()
            strategies = hook_type.strategies.filter(
                created_by__in=[1, user.id] if user else [1],
                enable=const.HOOK_TYPE_ENABLE).values()
            for strategy in strategies:
                profiles.append({
                    'type': hook_type.type,
                    "source": strategy.get("source"),
                    "target": strategy.get("target"),
                    "signature": strategy.get("value"),
                    "inherit": strategy.get("inherit")
                })
        return profiles
