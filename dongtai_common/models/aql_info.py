#!/usr/bin/env python
# datetime:2020/8/20 15:10

from django.db import models
from dongtai_common.models.agent import IastAgent
from dongtai_common.models.hook_type import HookType
from dongtai_common.models.vul_level import IastVulLevel
from dongtai_common.utils.settings import get_managed
from dongtai_web.dongtai_sca.models import VulPackage


class AqlInfo(models.Model):
    vul_title = models.CharField(max_length=255, blank=True, null=True)
    safe_version = models.CharField(max_length=255, blank=True, null=True)
    latest_version = models.CharField(max_length=255, blank=True, null=True)
    source_license = models.CharField(max_length=255, blank=True, null=True)
    aql = models.CharField(max_length=255, blank=True, null=True)

    availability = models.SmallIntegerField(blank=True, null=True)
    license_risk = models.SmallIntegerField(blank=True, null=True)
    vul_type_name = models.CharField(max_length=255, blank=True, null=True)
    level = models.ForeignKey(IastVulLevel, models.DO_NOTHING, blank=True, null=True)
    cve_relation_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = get_managed()
        db_table = "iast_aql_info"
