from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "scripts to deal with old data to new version"
    functions = []

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        from dongtai_web.dongtai_sca.tasks import refresh_all_asset_data

        refresh_all_asset_data()
        self.stdout.write(self.style.SUCCESS('Successfully flash old data  "{}"'.format("123123213321")))
