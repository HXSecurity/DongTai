#!/usr/bin/env python
# datetime:2020/8/26 16:01
from django.db import models

from dongtai_common.utils.settings import get_managed


class ImportFrom(models.IntegerChoices):
    SYSTEM = 1
    USER = 2
    __empty__ = 2


class ScaMavenDb(models.Model):
    group_id = models.CharField(max_length=255, blank=True, null=True)
    atrifact_id = models.CharField(max_length=255, blank=True, null=True)
    version = models.CharField(max_length=255, blank=True, null=True)
    sha_1 = models.CharField(unique=True, max_length=255, blank=True, null=True)
    package_name = models.CharField(max_length=255, blank=True, null=True)
    aql = models.CharField(max_length=255, blank=True, null=True)
    license = models.CharField(max_length=255, blank=True, null=True)
    import_from = models.IntegerField(
        choices=ImportFrom.choices, default=ImportFrom.USER
    )

    class Meta:
        managed = get_managed()
        db_table = "sca_maven_db"
