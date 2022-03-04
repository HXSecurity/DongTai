from django.apps import AppConfig
from utils import DongTaiAppConfigPatch


class ApiserverConfig(DongTaiAppConfigPatch, AppConfig):
    name = 'apiserver'
