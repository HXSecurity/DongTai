from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "scripts to deal with old data to new version"
    functions = []

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        from time import time

        from django.db.models import Q
        from rest_framework.authtoken.models import Token

        from dongtai_common.models import User
        from dongtai_common.models.department import Department

        users = User.objects.filter(~Q(pk=1)).all()
        timestamp = int(time())
        for user in users:
            parent = user.get_department()
            department = Department(
                name=user.username,
                create_time=timestamp,
                update_time=timestamp,
                created_by=user.id,
                parent_id=parent.id if parent else -1,
                principal_id=user.id,
            )
            department.token = Token.generate_key()
            department.save()
            if parent:
                if parent.department_path:
                    department.department_path = (
                        f"{parent.department_path}~{department.id}"
                    )
                else:
                    parent.department_path = f"{parent.id}"
                    parent.save()
                department.department_path = f"{parent.department_path}~{department.id}"
            else:
                department.department_path = f"{department.id}"
            department.save()
            talent = user.get_talent()
            talent.departments.add(department)
            user.department.set([department])
            user.save()
            self.stdout.write(
                self.style.SUCCESS(
                    'Successfully flash old data  "{}"'.format("department is update")
                )
            )
