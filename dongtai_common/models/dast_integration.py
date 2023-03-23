from dongtai_common.models.vulnerablity import IastVulnerabilityModel
from django.db import models
from dongtai_common.utils.settings import get_managed
from dongtai_common.models.project import IastProject
from dongtai_common.models.project_version import IastProjectVersion
from dongtai_common.models.vul_level import IastVulLevel
import time


class IastDastIntegration(models.Model):
    vul_name = models.CharField(max_length=255, blank=True, null=True)
    detail = models.TextField(
        blank=True,
        null=True,
        default='',
    )
    vul_level = models.ForeignKey(IastVulLevel,
                                  models.DO_NOTHING,
                                  blank=True,
                                  null=True)
    payload = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default='',
    )
    target = models.CharField(max_length=255, blank=True, null=True)
    vul_type = models.CharField(max_length=255, blank=True, null=True)
    dast_tag = models.CharField(max_length=255, blank=True, null=True)
    request_messages = models.JSONField(null=False, default=list)
    urls = models.JSONField(null=False, default=list)
    create_time = models.IntegerField(default=lambda: int(time.time()),
                                      blank=True,
                                      null=True)
    latest_time = models.IntegerField(default=lambda: int(time.time()),
                                      blank=True,
                                      null=True)
    project = models.ForeignKey(IastProject,
                                on_delete=models.CASCADE,
                                blank=True,
                                null=True,
                                default=-1)
    project_version = models.ForeignKey(IastProjectVersion,
                                        on_delete=models.CASCADE,
                                        blank=True,
                                        null=True,
                                        default=-1)
    dongtai_vul_type = models.JSONField(null=False, default=list)

    class Meta:
        managed = get_managed()
        db_table = 'iast_dast_integration'


class IastDastIntegrationRelation(models.Model):
    dt_mark = models.CharField(max_length=255, blank=True, null=True)
    iastvul = models.ForeignKey(IastVulnerabilityModel,
                                on_delete=models.CASCADE,
                                blank=True,
                                null=True,
                                default=-1)
    dastvul = models.ForeignKey(IastDastIntegration,
                                on_delete=models.CASCADE,
                                blank=True,
                                null=True,
                                default=-1)

    class Meta:
        managed = get_managed()
        db_table = 'iast_dast_integration_relation'


class IastvulDtMarkRelation(models.Model):
    dt_mark = models.CharField(max_length=255, blank=True, null=True)
    iastvul = models.ForeignKey(IastVulnerabilityModel,
                                on_delete=models.CASCADE,
                                blank=True,
                                null=True,
                                default=-1)

    class Meta:
        managed = get_managed()
        db_table = 'iast_iast_dtmatk_relation'


class DastvulDtMarkRelation(models.Model):
    dt_mark = models.CharField(max_length=255, blank=True, null=True)
    dastvul = models.ForeignKey(IastDastIntegration,
                                on_delete=models.CASCADE,
                                blank=True,
                                null=True,
                                default=-1)

    class Meta:
        managed = get_managed()
        db_table = 'iast_dast_dtmatk_relation'
