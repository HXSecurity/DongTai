from django.apps import AppConfig

from dongtai_common.common.utils import DongTaiAppConfigPatch


class IastConfig(DongTaiAppConfigPatch, AppConfig):
    name = "dongtai_web"

    def ready(self):
        super().ready()
        register_preheat()
        from deploy.commands.management.commands.load_hook_strategy import Command
        from dongtai_common.utils.init_schema import init_schema
        from dongtai_common.utils.validate import validate_hook_strategy_update
        from dongtai_conf.celery import app as celery_app
        from dongtai_conf.settings import AUTO_UPDATE_HOOK_STRATEGY

        # do not remove this import, used in celery
        from dongtai_engine.plugins.project_status import update_project_status

        if AUTO_UPDATE_HOOK_STRATEGY and not validate_hook_strategy_update():
            print("enable auto_update_hook_strategy  updating hook strategy from file")
            Command().handle()

        init_schema()


def register_preheat():
    from dongtai_engine.preheat import PreHeatRegister
    from dongtai_web.aggr_vul.aggr_vul_summary import get_annotate_sca_cache_data

    PreHeatRegister.register(get_annotate_sca_cache_data)
