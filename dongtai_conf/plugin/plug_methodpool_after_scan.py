from dongtai_conf.plugin import DongTaiPlugin
import json
from dongtai_common.models.agent_method_pool import MethodPool
from django.db.models import F
import logging

logger = logging.getLogger("dongtai-webapi")


def delete_model(method_pool: MethodPool) -> None:
    method_pool.delete()


class PlugMethodPoolAfterScan(DongTaiPlugin):
    appname = "dongtai_common"
    target_func_name = "method_pool_after_scan"
    target_module_name = "dongtai_engine.plugins.method_pool"
    plugin_type = 2

    def before_patch_function(self, func_args, func_kwargs):
        pass

    def after_patch_function(self, func_args, func_kwargs, func_res):
        return delete_model(*func_args, **func_kwargs)
