class DongTaiAppConfigPatch():
    def ready(self):
        try:
            from plugin import monkey_patch
            monkey_patch(self.name)
        except ImportError as e:
            print(e)
            pass
