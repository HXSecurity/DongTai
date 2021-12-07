from utils import DongTaiAppConfigPatch
from django.apps import AppConfig


class IastConfig(DongTaiAppConfigPatch, AppConfig):
    name = 'iast'
