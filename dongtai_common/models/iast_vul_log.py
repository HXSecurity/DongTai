from django.db import models

from dongtai_common.models.agent import IastAgent
from dongtai_common.utils.settings import get_managed
from django.db.models import IntegerChoices
from dongtai_common.models.user import User
from dongtai_common.models.asset import Asset
from dongtai_common.models.vulnerablity import IastVulnerabilityModel
from time import time
from dongtai_common.models.asset_vul import IastAssetVul, IastVulAssetRelation


class MessageTypeChoices(IntegerChoices):
    CHANGE_STATUS = 1
    VUL_RECHECK = 2
    PUSH_TO_INTEGRATION = 3
    VUL_FOUND = 4


class IastVulLog(models.Model):
    msg_type = models.IntegerField(blank=True, null=True)
    msg = models.TextField(blank=True, null=True)
    meta_data = models.JSONField(blank=True, null=True)
    datetime = models.IntegerField(blank=True, null=True, default=time())
    vul = models.ForeignKey(IastVulnerabilityModel,
                                models.DO_NOTHING,
                                default=-1,
                                db_constraint=False)
    asset_vul = models.ForeignKey(IastAssetVul,
                                      models.DO_NOTHING,
                                      default=-1,
                                      db_constraint=False)
    user = models.ForeignKey(User, models.DO_NOTHING, db_constraint=False)

    class Meta:
        managed = get_managed()
        db_table = 'iast_vul_log'
