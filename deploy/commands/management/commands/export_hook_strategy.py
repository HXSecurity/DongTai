from django.core.management.base import BaseCommand
from dongtai_common.models.agent_method_pool import MethodPool
from dongtai_protocol.views.hook_profiles import HookProfilesEndPoint, LANGUAGE_DICT
import json
from dongtai_conf.settings import BASE_DIR
import os
from dongtai_common.models.strategy import IastStrategyModel


def export_strategy():
    pass

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

        self.stdout.write(
            self.style.SUCCESS('Successfully export strategy .'))
