from django.db import models

from dongtai_common.models import User
from dongtai_common.models.asset_vul import IastAssetVul
from dongtai_common.models.vulnerablity import IastVulnerabilityModel
from dongtai_common.utils.settings import get_managed


class IastVulInegration(models.Model):
    user = models.ForeignKey(to=User,
                             on_delete=models.DO_NOTHING,
                             blank=True,
                             null=True)
    vul = models.ForeignKey(to=IastVulnerabilityModel,
                            on_delete=models.DO_NOTHING,
                            blank=True,
                            null=True,
                            default=-1)
    asset_vul = models.ForeignKey(to=IastAssetVul,
                                  on_delete=models.DO_NOTHING,
                                  blank=True,
                                  default=-1)
    jira_url = models.CharField(default="", blank=True, null=True,max_length=255)
    jira_id = models.CharField(default="", blank=True, null=True,max_length=255)
    jira_state = models.CharField(default="", blank=True, null=True,max_length=20)
    gitlab_url = models.CharField(default="", blank=True, null=True,max_length=255)
    gitlab_id = models.CharField(default="", blank=True, null=True,max_length=255)
    gitlab_state = models.CharField(default="", blank=True, null=True,max_length=20)
    zendao_url = models.CharField(default="", blank=True, null=True,max_length=255)
    zendao_id = models.CharField(default="", blank=True, null=True,max_length=255)
    zendao_state = models.CharField(default="", blank=True, null=True,max_length=20)

    class Meta:
        managed = get_managed()
        db_table = "iast_vul_integration"
