from dongtai_common.models.vulnerablity import IastVulnerabilityModel
from django.db import models
from dongtai_common.utils.settings import get_managed


class IastDastIntegration(models.Model):
    vul = models.ForeignKey(
        IastVulnerabilityModel,
        models.DO_NOTHING,
        blank=True,
        null=True,
    )
    uuid = models.CharField(max_length=255, blank=True, null=True)
    data = models.JSONField(null=False, default={})

    class Meta:
        managed = get_managed()
        db_table = 'iast_dast_integration'
