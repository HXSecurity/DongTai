from django.apps import AppConfig


class VulnConfig(AppConfig):
    name = 'vuln'

    def ready(self):
        from signals.handlers import save_vul
        from signals import vul_found
