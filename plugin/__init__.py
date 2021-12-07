

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
    pass
