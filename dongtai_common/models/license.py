from django.db import models

# Create your models here.
from django.db import models
from dongtai_common.utils.settings import get_managed


class IastLicense(models.Model):
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        db_table = 'iast_license'
