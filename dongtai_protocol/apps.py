from django.apps import AppConfig
from dongtai.common.utils import DongTaiAppConfigPatch


class ApiserverConfig(DongTaiAppConfigPatch, AppConfig):
    name = 'dongtai_protocol'
