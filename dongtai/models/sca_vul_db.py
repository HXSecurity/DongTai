#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/8/26 16:01
# software: PyCharm
# project: dongtai-models
from django.db import models
from dongtai.utils.settings import get_managed


class ScaVulDb(models.Model):
    package_type = models.CharField(max_length=20, blank=True, null=True)
    cve = models.CharField(max_length=20, blank=True, null=True)
    cwe = models.CharField(max_length=20, blank=True, null=True)
    vul_name = models.CharField(max_length=255, blank=True, null=True)
    vul_level = models.CharField(max_length=20, blank=True, null=True)
    cve_href = models.CharField(max_length=255, blank=True, null=True)
    cwe_href = models.CharField(max_length=255, blank=True, null=True)
    aql = models.CharField(max_length=255, blank=True, null=True)
    version_range = models.CharField(max_length=255, blank=True, null=True)
    version_condition = models.CharField(max_length=255, blank=True, null=True)
    latest_version = models.CharField(max_length=255, blank=True, null=True)
    overview = models.CharField(max_length=255, blank=True, null=True)
    teardown = models.CharField(max_length=2000, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    source = models.CharField(max_length=20, blank=True, null=True)
    dt = models.IntegerField(blank=True, null=True)
    extra = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = get_managed()
        db_table = 'sca_vul_db'
