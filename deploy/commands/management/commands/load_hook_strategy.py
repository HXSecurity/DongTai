import json
import os
from collections import OrderedDict

from django.core.management.base import BaseCommand
from django.db.models import Q

from dongtai_common.models.hook_strategy import HookStrategy
from dongtai_common.models.hook_type import HookType
from dongtai_common.models.sensitive_info import IastSensitiveInfoRule
from dongtai_common.models.strategy import IastStrategyModel
from dongtai_common.utils.validate import save_hook_stratefile_sha1sum
from dongtai_conf.settings import BASE_DIR
from dongtai_protocol.views.hook_profiles import LANGUAGE_DICT


class Command(BaseCommand):
    help = "load hook_strategy"
    functions = []

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        POLICY_DIR = os.path.join(BASE_DIR, "static/data/")
        with open(os.path.join(POLICY_DIR, "vul_strategy.json")) as fp:
            full_strategies = json.load(fp, object_pairs_hook=OrderedDict)
        if os.path.exists(os.path.join(POLICY_DIR, "sensitive_info_strategy.json")):
            with open(os.path.join(POLICY_DIR, "sensitive_info_strategy.json")) as fp:
                full_strategies.extend(json.load(fp, object_pairs_hook=OrderedDict))
        strategy_dict = {}
        for strategy in full_strategies:
            if IastStrategyModel.objects.filter(
                vul_type=strategy["vul_type"],
                system_type=1,
            ).exists():
                # 已存在策略类型,不会重建
                IastStrategyModel.objects.filter(
                    vul_type=strategy["vul_type"],
                    system_type=1,
                ).update(
                    **{
                        your_key: strategy[your_key]
                        for your_key in [
                            "vul_desc",
                            "vul_desc_en",
                            "vul_desc_zh",
                            "vul_fix",
                            "vul_fix_en",
                            "vul_fix_zh",
                            "vul_name",
                            "vul_name_en",
                            "vul_name_zh",
                            "level",
                        ]
                    }
                )
                qs1 = IastStrategyModel.objects.filter(
                    vul_type=strategy["vul_type"],
                    system_type=1,
                ).values_list("id", flat=True)
                strategy_obj = IastStrategyModel.objects.filter(pk__in=qs1).order_by("id").first()
                strategy_dict[strategy["vul_type"]] = strategy_obj
                continue
            if (
                IastStrategyModel.objects.filter(
                    vul_type=strategy["vul_type"],
                    system_type=0,
                ).exists()
                or IastStrategyModel.objects.filter(
                    vul_type=strategy["vul_type"],
                    iastsensitiveinforule__id__isnull=False,
                    system_type=0,
                ).exists()
            ):
                # 存在用户定义的冲突策略,不会修改
                continue
            strategy["user_id"] = strategy["user"]
            del strategy["user"]
            strategy["level_id"] = strategy["level"]
            del strategy["level"]
            strategy_obj = IastStrategyModel.objects.create(**strategy)
            strategy_dict[strategy["vul_type"]] = strategy_obj
        for k, v in LANGUAGE_DICT.items():
            with open(os.path.join(POLICY_DIR, f"{k.lower()}_hooktype.json")) as fp:
                hooktypes = json.load(fp, object_pairs_hook=OrderedDict)
            hooktype_dict = {}
            for hook_type in hooktypes:
                if HookType.objects.filter(
                    value=hook_type["value"],
                    type=hook_type["type"],
                    language_id=v,
                    system_type=1,
                ).exists():
                    # 已存在策略类型,不会重建,会将新的规则添加到这上边
                    hooktype_obj = HookType.objects.filter(
                        value=hook_type["value"],
                        language_id=v,
                        type=hook_type["type"],
                        system_type=1,
                    ).first()
                    hooktype_dict[f"{hook_type['value']}-{hook_type['type']}"] = hooktype_obj
                    continue
                if HookType.objects.filter(
                    value=hook_type["value"],
                    type=hook_type["type"],
                    language_id=v,
                    system_type=0,
                ).exists():
                    # 存在用户定义的冲突策略,不会修改
                    continue
                del hook_type["language"]
                hook_type["language_id"] = v
                hooktype_obj = HookType(**hook_type)
                hooktype_obj.save()
                hooktype_dict[f"{hook_type['value']}-{hook_type['type']}"] = hooktype_obj

            with open(os.path.join(POLICY_DIR, f"{k.lower()}_full_policy.json")) as fp:
                full_policy = json.load(fp, object_pairs_hook=OrderedDict)
            for policy in full_policy:
                if policy["type"] == 4:
                    if policy["value"] not in strategy_dict:
                        continue
                    policy_strategy = strategy_dict[policy["value"]]
                    for hook_strategy in policy["details"]:
                        if HookStrategy.objects.filter(
                            value=hook_strategy["value"], type=hook_strategy["type"], language_id=v, system_type=1
                        ).exists():
                            # 如果已经存在规则,跳过创建
                            continue
                        if HookStrategy.objects.filter(
                            value=hook_strategy["value"], type=hook_strategy["type"], language_id=v, system_type=0
                        ):
                            # 如果已经存在用户自定义规则,设置为系统规则,跳过创建
                            hook_strategy_obj = HookStrategy.objects.filter(
                                value=hook_strategy["value"], type=hook_strategy["type"], language_id=v, system_type=0
                            ).get()
                            hook_strategy_obj.system_type = 1
                            hook_strategy_obj.save()
                            continue
                        del hook_strategy["language"]
                        hook_strategy["language_id"] = v
                        HookStrategy.objects.create(strategy=policy_strategy, **hook_strategy)
                else:
                    if f"{policy['value']}-{policy['type']}" not in hooktype_dict:
                        continue
                    policy_hook_type = hooktype_dict[f"{policy['value']}-{policy['type']}"]
                    for hook_strategy in policy["details"]:
                        if HookStrategy.objects.filter(
                            value=hook_strategy["value"], type=hook_strategy["type"], language_id=v, system_type=1
                        ).exists():
                            # 如果已经存在规则,跳过创建
                            continue
                        if HookStrategy.objects.filter(
                            value=hook_strategy["value"], type=hook_strategy["type"], language_id=v, system_type=0
                        ):
                            # 如果已经存在用户自定义规则,设置为系统规则,跳过创建
                            hook_strategy_obj = HookStrategy.objects.filter(
                                value=hook_strategy["value"], type=hook_strategy["type"], language_id=v, system_type=0
                            ).get()
                            hook_strategy_obj.system_type = 1
                            hook_strategy_obj.save()
                            continue
                        del hook_strategy["language"]
                        hook_strategy["language_id"] = v
                        HookStrategy.objects.create(hooktype=policy_hook_type, **hook_strategy)
        save_hook_stratefile_sha1sum()

        sensitive_info_rule = []
        if os.path.exists(os.path.join(POLICY_DIR, "sensitive_info_rule.json")):
            with open(os.path.join(POLICY_DIR, "sensitive_info_rule.json")) as fp:
                sensitive_info_rule = json.load(fp, object_pairs_hook=OrderedDict)
        sensitive_info_rule_ids = []
        for rule in sensitive_info_rule:
            if rule["strategy"] not in strategy_dict:
                continue
            strategy = strategy_dict[rule["strategy"]]
            exist_rule = IastSensitiveInfoRule.objects.filter(
                strategy=strategy, pattern_type_id=rule["pattern_type"], pattern=rule["pattern"], system_type=1
            ).first()
            if exist_rule:
                sensitive_info_rule_ids.append(exist_rule.pk)
            else:
                obj = IastSensitiveInfoRule.objects.create(
                    user_id=1,
                    strategy=strategy,
                    pattern_type_id=rule["pattern_type"],
                    pattern=rule["pattern"],
                    status=1,
                    system_type=1,
                )
                sensitive_info_rule_ids.append(obj.pk)
        IastSensitiveInfoRule.objects.filter(~Q(id__in=sensitive_info_rule_ids), system_type=1).delete()
        self.stdout.write(self.style.SUCCESS("Successfully load strategy ."))
