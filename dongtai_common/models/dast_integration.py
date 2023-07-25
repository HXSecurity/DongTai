
from django.db import models

from dongtai_common.models.project import IastProject
from dongtai_common.models.project_version import IastProjectVersion
from dongtai_common.models.vul_level import IastVulLevel
from dongtai_common.models.vulnerablity import IastVulnerabilityModel
from dongtai_common.utils.db import get_timestamp
from dongtai_common.utils.settings import get_managed


class IastDastIntegration(models.Model):
    vul_name = models.CharField(max_length=255, blank=True)
    detail = models.TextField(blank=True)
    vul_level = models.ForeignKey(IastVulLevel, models.DO_NOTHING, blank=True)
    payload = models.CharField(max_length=255, blank=True)
    target = models.CharField(max_length=255, blank=True)
    vul_type = models.CharField(max_length=255, blank=True)
    dast_tag = models.CharField(max_length=255, blank=True)
    request_messages = models.JSONField(default=list)
    urls = models.JSONField(default=list)
    create_time = models.IntegerField(default=get_timestamp, blank=True)
    latest_time = models.IntegerField(default=get_timestamp, blank=True)
    project = models.ForeignKey(IastProject, on_delete=models.CASCADE, blank=True, default=-1)
    project_version = models.ForeignKey(IastProjectVersion, on_delete=models.CASCADE, blank=True, default=-1)
    dongtai_vul_type = models.JSONField(default=list)

    class Meta:
        managed = get_managed()
        db_table = "iast_dast_integration"


class IastDastIntegrationRelation(models.Model):
    dt_mark = models.CharField(max_length=255, blank=True)
    iastvul = models.ForeignKey(IastVulnerabilityModel, on_delete=models.CASCADE, blank=True, default=-1)
    dastvul = models.ForeignKey(IastDastIntegration, on_delete=models.CASCADE, blank=True, default=-1)

    class Meta:
        managed = get_managed()
        db_table = "iast_dast_integration_relation"


class IastvulDtMarkRelation(models.Model):
    dt_mark = models.CharField(max_length=255, blank=True)
    iastvul = models.ForeignKey(IastVulnerabilityModel, on_delete=models.CASCADE, blank=True, default=-1)

    class Meta:
        managed = get_managed()
        db_table = "iast_iast_dtmatk_relation"


class DastvulDtMarkRelation(models.Model):
    dt_mark = models.CharField(max_length=255, blank=True)
    dastvul = models.ForeignKey(IastDastIntegration, on_delete=models.CASCADE, blank=True, default=-1)

    class Meta:
        managed = get_managed()
        db_table = "iast_dast_dtmatk_relation"
