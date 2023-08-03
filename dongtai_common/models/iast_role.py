from django.db import models

from dongtai_common.utils.settings import get_managed


class RoleStatus(models.IntegerChoices):
    DISABLE = 0, "禁用"
    ENABLE = 1, "启用"


class IastRoleV2(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    is_admin = models.BooleanField(default=False)
    is_preset = models.BooleanField(default=False)
    permission = models.JSONField()
    status = models.IntegerField(choices=RoleStatus.choices)

    class Meta:
        managed = get_managed()
        db_table = "iast_role"
        indexes = [models.Index(fields=["name"])]
