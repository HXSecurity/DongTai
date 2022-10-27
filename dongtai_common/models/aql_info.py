#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/8/20 15:10
# software: PyCharm
# project: dongtai-models

from django.db import models
from dongtai_common.models.agent import IastAgent
from dongtai_common.models.hook_type import HookType
from dongtai_common.models.vul_level import IastVulLevel
from dongtai_common.utils.settings import get_managed
from dongtai_web.dongtai_sca.models import VulPackage


from _typeshed import Incomplete
class AqlInfo(models.Model):

    vul_title: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    safe_version: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    latest_version: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    source_license: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    aql: Incomplete = models.CharField(max_length=255, blank=True, null=True)

    availability: Incomplete = models.SmallIntegerField(blank=True, null=True)
    license_risk: Incomplete = models.SmallIntegerField(blank=True, null=True)
    vul_type_name: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    level: Incomplete = models.ForeignKey(IastVulLevel, models.DO_NOTHING, blank=True, null=True)
    cve_relation_id: Incomplete = models.IntegerField(blank=True, null=True)


    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'iast_aql_info'
