from django.apps import AppConfig

from dongtai_common.common.utils import DongTaiAppConfigPatch


class DongTaiConfig(DongTaiAppConfigPatch, AppConfig):
    name = "dongtai_common"
