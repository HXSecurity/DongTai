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
from collections import defaultdict

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
        allstrategies = list(
            HookStrategy.objects.filter(
                (Q(hooktype__in=hook_types_a) | Q(strategy__in=hook_types))
                & Q(enable=const.HOOK_TYPE_ENABLE, language_id=language_id)).
            values().all())

        sink_strategies_dict = defaultdict(list)
        other_strategies_dict = defaultdict(list)
        for strategy in allstrategies:
            if strategy['type'] == 4:
                sink_strategies_dict[strategy['strategy_id']].append(strategy)
            else:
                other_strategies_dict[strategy['hooktype_id']].append(strategy)

        for hook_type in list(hook_types) + list(hook_types_a):
            strategy_details = list()
            if isinstance(hook_type, IastStrategyModel):
                hook_type = convert_strategy(hook_type)
                strategies = sink_strategies_dict[hook_type.id]
            else:
                strategies = other_strategies_dict[hook_type.id]

            for strategy in strategies:
                profiles.append({
                    'type':
                    hook_type.type,
                    'vul_type':
                    hook_type.value,
                    "source":
                    strategy.get("source"),
                    "target":
                    strategy.get("target"),
                    "signature":
                    strategy.get("value"),
                    "inherit":
                    strategy.get("inherit"),
                    "ignore_blacklist":
                    strategy.get("ignore_blacklist"),
                    "ignore_internal":
                    strategy.get("ignore_internal"),
                    "tags":
                    strategy.get("tags"),
                    "untags":
                    strategy.get("untags"),
                    "command":
                    strategy.get("command"),
                    "stack_blacklist":
                    strategy.get("stack_blacklist"),
                })
        return profiles
