from django.core.management.base import BaseCommand
from dongtai_common.models.agent_method_pool import MethodPool
from dongtai_protocol.views.hook_profiles import HookProfilesEndPoint, LANGUAGE_DICT
import json
from dongtai_conf.settings import BASE_DIR
import os
from dongtai_common.models.strategy import IastStrategyModel
from dongtai_common.models.sensitive_info import IastSensitiveInfoRule
from dongtai_common.models.hook_strategy import HookStrategy
from dongtai_common.models.hook_type import HookType
from django.forms.models import model_to_dict


def transform_hooktype(hook_type: HookType) -> HookType:
    hook_type.enable = 1
    return hook_type


def export_strategy() -> list:
    strategies = (
        IastStrategyModel.objects.filter(user_id=1, state__in=["enable", "disable"])
        .order_by("id")
        .all()
    )

    strategies_res = sorted(
        [
            model_to_dict(
                i,
                exclude=[
                    "id",
                    "hook_type",
                    "vul_strategy",
                    "create_time",
                    "update_time",
                    "dt",
                ],
            )
            for i in strategies
        ],
        key=lambda item: item["vul_type"],
    )
    return strategies_res


def export_hooktype(language_id: int) -> list:
    qs1 = HookType.objects.filter(
        language_id=language_id,
        enable__in=[0, 1],
        created_by__in=[1],
    ).values_list("id", flat=True)
    strategies = (
        HookType.objects.filter(
            language_id=language_id, created_by__in=[1], pk__in=list(qs1)
        )
        .order_by("id")
        .all()
    )

    strategies = map(transform_hooktype, list(strategies))
    strategies_res = sorted(
        [
            model_to_dict(
                i,
                exclude=[
                    "id",
                    "hook_type",
                    "vul_strategy",
                    "create_time",
                    "update_time",
                    "dt",
                ],
            )
            for i in strategies
        ],
        key=lambda item: item["value"],
    )
    return strategies_res


class Command(BaseCommand):
    help = "export all hook_strategy"
    functions = []

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        POLICY_DIR = os.path.join(BASE_DIR, "static/data/")
        for k, v in LANGUAGE_DICT.items():
            c = HookProfilesEndPoint.get_profiles(language_id=v, system_only=True)
            with open(os.path.join(POLICY_DIR, f"{k.lower()}_policy.json"), "w+") as fp:
                json.dump(c, fp, indent=4, sort_keys=True)

            c = HookProfilesEndPoint.get_profiles(
                language_id=v, full=True, system_only=True
            )
            with open(
                os.path.join(POLICY_DIR, f"{k.lower()}_full_policy.json"), "w+"
            ) as fp:
                json.dump(c, fp, indent=4, sort_keys=True)
            with open(
                os.path.join(POLICY_DIR, f"{k.lower()}_hooktype.json"), "w+"
            ) as fp:
                json.dump(export_hooktype(language_id=v), fp, indent=4, sort_keys=True)
        with open(os.path.join(POLICY_DIR, f"vul_strategy.json"), "w+") as fp:
            json.dump(export_strategy(), fp, indent=4, sort_keys=True)

        self.stdout.write(self.style.SUCCESS("Successfully export strategy ."))
