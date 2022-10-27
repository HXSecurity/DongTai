from django.apps import AppConfig
from dongtai_common.common.utils import DongTaiAppConfigPatch


class ApiserverConfig(DongTaiAppConfigPatch, AppConfig):
    name: str = 'dongtai_protocol'
