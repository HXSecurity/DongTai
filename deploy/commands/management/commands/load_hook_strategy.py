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
from collections import OrderedDict

class Command(BaseCommand):
    help = 'load hook_strategy'
    functions = []

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        POLICY_DIR = os.path.join(BASE_DIR, 'static/data/')
        with open(os.path.join(POLICY_DIR, f'vul_strategy.json')) as fp:
            full_strategies = json.load(fp,object_pairs_hook=OrderedDict)
        strategy_dict = {}
        for strategy in full_strategies:
            if IastStrategyModel.objects.filter(
                    vul_type=strategy['vul_type'],
                    strategy__id__isnull=False,
                    system_type=1,
            ).exists() or IastStrategyModel.objects.filter(
                    vul_type=strategy['vul_type'],
                    iastsensitiveinforule__id__isnull=False,
                    system_type=1).exists():
                #已存在策略类型，不会重建
                qs1 = IastStrategyModel.objects.filter(
                    vul_type=strategy['vul_type'],
                    system_type=1,
                    strategy__id__isnull=False).values_list('id', flat=True)
                qs2 = IastStrategyModel.objects.filter(
                    vul_type=strategy['vul_type'],
                    system_type=1,
                    iastsensitiveinforule__id__isnull=False).values_list(
                        'id', flat=True)
                strategy_obj = IastStrategyModel.objects.filter(
                    pk__in=list(qs1.union(qs2))).order_by('id').first()
                strategy_dict[strategy['vul_type']] = strategy_obj
                continue
            if IastStrategyModel.objects.filter(
                    vul_type=strategy['vul_type'],
                    strategy__id__isnull=False,
                    system_type=0).exists(
                    ) or IastStrategyModel.objects.filter(
                        vul_type=strategy['vul_type'],
                        iastsensitiveinforule__id__isnull=False,
                        system_type=0).exists():
                #存在用户定义的冲突策略,不会修改
                continue
            #strategy['language_id'] = strategy['language']
            #del strategy['language']
            strategy['user_id'] = strategy['user']
            del strategy['user']
            strategy['level_id'] = strategy['level']
            del strategy['level']
            strategy_obj = IastStrategyModel.objects.create(**strategy)
            strategy_dict[strategy['vul_type']] = strategy_obj
        for k, v in LANGUAGE_DICT.items():
            with open(os.path.join(POLICY_DIR,
                                   f'{k.lower()}_hooktype.json')) as fp:
                hooktypes = json.load(fp, object_pairs_hook=OrderedDict)
            hooktype_dict = {}
            for hook_type in hooktypes:
                if HookType.objects.filter(value=hook_type['value'],
                                           strategy__id__isnull=False,
                                           type=hook_type['type'],
                                           system_type=1).exists():
                    #已存在策略类型，不会重建,会将新的规则添加到这上边
                    hooktype_obj = HookType.objects.filter(
                        value=hook_type['value'],
                        language_id=v,
                        type=hook_type['type'],
                        strategy__id__isnull=False,
                        system_type=1).first()
                    hooktype_dict[f"{hook_type['value']}-{hook_type['type']}"] = hooktype_obj
                    continue
                if HookType.objects.filter(value=hook_type['value'],
                                           strategy__id__isnull=False,
                                           type=hook_type['type'],
                                           language_id=v,
                                           system_type=0).exists():
                    #存在用户定义的冲突策略,不会修改
                    continue
                #del hook_type['created_by']
                del hook_type['language']
                hook_type['language_id'] = v
                hooktype_obj = HookType(**hook_type)
                hooktype_obj.save()
                hooktype_dict[f"{hook_type['value']}-{hook_type['type']}"] = hooktype_obj

            HookStrategy.objects.filter(language_id=v, system_type=1).delete()
            with open(os.path.join(POLICY_DIR,
                                   f'{k.lower()}_full_policy.json')) as fp:
                full_policy = json.load(fp, object_pairs_hook=OrderedDict)
            for policy in full_policy:
                if policy['type'] == 4:
                    if policy['value'] not in strategy_dict.keys():
                        continue
                    policy_strategy = strategy_dict[policy['value']]
                    for hook_strategy in policy['details']:
                        del hook_strategy['language']
                        hook_strategy['language_id'] = v
                        HookStrategy.objects.create(strategy=policy_strategy,
                                                    **hook_strategy)
                else:
                    if policy['value'] not in hooktype_dict.keys():
                        continue
                    policy_hook_type = hooktype_dict[
                        f"{policy['value']}-{policy['type']}"]
                    for hook_strategy in policy['details']:
                        del hook_strategy['language']
                        hook_strategy['language_id'] = v
                        HookStrategy.objects.create(hooktype=policy_hook_type,
                                                    **hook_strategy)
        self.stdout.write(self.style.SUCCESS('Successfully load strategy .'))
