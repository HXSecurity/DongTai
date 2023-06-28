from django.db import models
from dongtai_common.utils.settings import get_managed


class IastProfile(models.Model):
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    class Meta:
        managed = get_managed()
        db_table = 'iast_profile'
