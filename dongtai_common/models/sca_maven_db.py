#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/8/26 16:01
# software: PyCharm
# project: dongtai-models
from django.db import models
from dongtai_common.utils.settings import get_managed


from _typeshed import Incomplete
class ImportFrom(models.IntegerChoices):
    SYSTEM: int = 1
    USER: int = 2
    __empty__: int = 2


class ScaMavenDb(models.Model):
    group_id: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    atrifact_id: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    version: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    sha_1: Incomplete = models.CharField(unique=True,
                             max_length=255,
                             blank=True,
                             null=True)
    package_name: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    aql: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    license: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    import_from: Incomplete = models.IntegerField(choices=ImportFrom.choices,
                                      default=ImportFrom.USER)

    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'sca_maven_db'
