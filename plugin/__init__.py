from AgentServer.settings import BASE_DIR
from os import walk, chdir, getcwd
from os.path import join
from importlib import import_module
from inspect import getmembers
from functools import wraps
PLUGIN_DICT = {}


class DongTaiPlugin:
    appname = 'appserver'
    target_class_name = 'SaasMethodPoolHandler'
    target_func_name = 'save_method_call'
    target_module_name = 'apiserver.report.handler.saas_method_pool_handler'

    def before_patch_function(self, func_args, func_kwargs):
        pass

    def after_patch_function(self, func_args, func_kwargs, func_res):
        pass

    def _monkey_patch(self):
        module = import_module(self.target_module_name)
        target_class = getattr(self.target_class_name, module)
        origin_func = getattr(target_class, self.target_func_name)
        setattr(target_class, f'_origin_{self.target_func_name}', origin_func)
        self.target_class = target_class

        @warps(origin_func)
        def patched_function(*args, **kwargs):
            DongTaiPlugin.before_patch_function(args, kwargs)
            res = getattr(self, f'_origin_{self.target_func_name}')(*args,
                                                                    **kwargs)
            final_res = DongTaiPlugin.after_patch_function(args, kwargs, res)
            return final_res

        setattr(SaasMethodPoolHandler, target_func_name,
                DongTaiPlugin.patched_function)

    def monkey_patch(self, appname):
        if self.appname == appname:
            self._monkey_patch()


def monkey_patch(appname):
    '''
    Register your monkeypatch here.
    Here is a sample.
    ============================================================
    if appname == 'iast':
        from iast.views.engine_method_pool_search import MethodPoolSearchProxy
        from dongtai.endpoint import R
        def cuspost(self, request):
            return R.success(msg='patched')
        MethodPoolSearchProxy.post = cuspost
    '''
    plugin_dict = get_plugin_dict()
    for plugin in plugin_dict.get(appname, []):
        plugin.monkey_patch(appname)


def get_plugin_dict():
    if PLUGIN_DICT:
        return PLUGIN_DICT
    previous_path = getcwd()
    PLUGIN_ROOT_PATH = join(BASE_DIR, 'plugin')
    for root, directories, files in walk(top=getcwd(), topdown=False):
        for file_ in files:
            if file_.startswith('plug_') and file_.endswith('.py'):
                mod = import_module(
                    root.replace(BASE_DIR, '').replace('/',
                                                       '.').replace('.py', ''))
                plugin_classes = filter(lambda x: _plug_class_filter(x),
                                        inspect.getmembers(mod))
                for name, plug_class in plugin_classes:
                    if PLUGIN_DICT.get(plug_class.appname):
                        PLUGIN_DICT[plug_class.appname] = [plug_class]
                    else:
                        PLUGIN_DICT[plug_class.appname] += [plug_class]
    chdir(previous_path)


def _plug_class_filter(tup):
    return tup[0].startswith('Plug') and inspect.isclass(
        tup[1]) and issubclass(tup[1], DongTaiPlugin)
