from django.db import models
from dongtai_common.utils.settings import get_managed

from _typeshed import Incomplete
class IastProfile(models.Model):
    key: Incomplete = models.CharField(max_length=100)
    value: Incomplete = models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'iast_profile'
