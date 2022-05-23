from utils import DongTaiAppConfigPatch
from django.apps import AppConfig


class IastConfig(DongTaiAppConfigPatch, AppConfig):
    name = "iast"

    def ready(self):
        super().ready()
        register_preheat()


def register_preheat():
    from core.preheat import PreHeatRegister

    from iast.aggr_vul.app_vul_summary import get_annotate_cache_data

    PreHeatRegister.register(get_annotate_cache_data)
