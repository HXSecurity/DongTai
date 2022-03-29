from django.apps import AppConfig


class VulnConfig(AppConfig):
    name = 'vuln'

    def ready(self):
        # 加载信号处理方法和信号
        from signals.handlers import vul_handler
        from signals import vul_found
