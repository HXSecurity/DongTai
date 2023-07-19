from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "scripts to deal with old data to new version 1.9.3."
    functions = []

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        from dongtai_web.projecttemplate.update_department_data import (
            update_department_data,
        )

        update_department_data()
        self.stdout.write(
            self.style.SUCCESS("Successfully flash old data department token.")
        )
