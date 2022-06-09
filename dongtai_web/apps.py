from dongtai_common.common.utils import DongTaiAppConfigPatch
from django.apps import AppConfig


class IastConfig(DongTaiAppConfigPatch, AppConfig):
    name = "dongtai_web"

    def ready(self):
        super().ready()
#        register_preheat()
        from dongtai_conf.celery import app as celery_app



#def register_preheat():
#    from dongtai_engine.preheat import PreHeatRegister
#
#    from dongtai_web.aggr_vul.app_vul_summary import get_annotate_cache_data
#
#    PreHeatRegister.register(get_annotate_cache_data)
