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


def export_strategy() -> list:
    qs1 = IastStrategyModel.objects.filter(
        strategy__id__isnull=False).values_list('id', flat=True)
    qs2 = IastStrategyModel.objects.filter(
        iastsensitiveinforule__id__isnull=False).values_list('id', flat=True)
    strategies = IastStrategyModel.objects.filter(
        pk__in=list(qs1.union(qs2))).order_by('id').all()

    strategies_res = [
        model_to_dict(i,
                      exclude=[
                          'id', 'hook_type', 'vul_strategy', 'create_time',
                          'update_time', 'dt'
                      ]) for i in strategies
    ]
    return strategies_res


def export_hooktype(language_id: int) -> list:
    qs1 = HookType.objects.filter(language_id=language_id,
                                  strategy__id__isnull=False).values_list(
                                      'id', flat=True)
    strategies = HookType.objects.filter(language_id=language_id,
                                         pk__in=list(qs1)).order_by('id').all()

    strategies_res = [
        model_to_dict(i,
                      exclude=[
                          'id', 'hook_type', 'vul_strategy', 'create_time',
                          'update_time', 'dt'
                      ]) for i in strategies
    ]
    return strategies_res

class Command(BaseCommand):
    help = 'export all hook_strategy'
    functions = []

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        POLICY_DIR = os.path.join(BASE_DIR,'static/data/')
        for k, v in LANGUAGE_DICT.items():
            c = HookProfilesEndPoint.get_profiles(language_id=v,
                                                  system_only=True)
            with open(os.path.join(POLICY_DIR, f'{k.lower()}_policy.json'),
                      'w+') as fp:
                json.dump(c, fp, indent=4)

            c = HookProfilesEndPoint.get_profiles(language_id=v,
                                                  full=True,
                                                  system_only=True)
            with open(
                    os.path.join(POLICY_DIR, f'{k.lower()}_full_policy.json'),
                    'w+') as fp:
                json.dump(c, fp, indent=4)
            with open(
                    os.path.join(POLICY_DIR, f'{k.lower()}_hooktype.json'),
                    'w+') as fp:
                json.dump(export_hooktype(language_id=v), fp, indent=4)
        with open(os.path.join(POLICY_DIR, f'vul_strategy.json'), 'w+') as fp:
            json.dump(export_strategy(), fp, indent=4)

        self.stdout.write(
            self.style.SUCCESS('Successfully export strategy .'))
