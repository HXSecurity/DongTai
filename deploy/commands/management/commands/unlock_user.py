from django.core.management.base import BaseCommand

from dongtai_common.models.user import User


class Command(BaseCommand):
    help = "scripts to unlock user"
    functions = []

    def add_arguments(self, parser):
        parser.add_argument("id", nargs="*", default=[], type=int)

    def handle(self, *args, **options):
        users = User.objects.filter(pk__in=options["id"]).all() if options["id"] else User.objects.all()
        users.update(failed_login_count=0)
        self.stdout.write(self.style.SUCCESS("Successfully Unlock Users"))
        self.stdout.write(self.style.NOTICE("除了使用这个命令外，您还可以通过配置 TOTP 快捷解锁管理员用户。"))
        self.stdout.write(
            self.style.NOTICE(
                "In addition to using this command, "
                "you can also configure TOTP to quickly unlock the administrator user."
            )
        )
