#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/8/26 16:01
# software: PyCharm
# project: dongtai-models
from django.db import models
from dongtai.utils.settings import get_managed


class ScaMavenDb(models.Model):
    group_id = models.CharField(max_length=255, blank=True, null=True)
    atrifact_id = models.CharField(max_length=255, blank=True, null=True)
    version = models.CharField(max_length=255, blank=True, null=True)
    sha_1 = models.CharField(unique=True, max_length=255, blank=True, null=True)
    package_name = models.CharField(max_length=255, blank=True, null=True)
    aql = models.CharField(max_length=255, blank=True, null=True)
    license = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = get_managed()
        db_table = 'sca_maven_db'
