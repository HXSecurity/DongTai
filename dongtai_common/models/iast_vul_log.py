from time import time

from django.db import models
from django.db.models import IntegerChoices

from dongtai_common.models.asset_vul import IastAssetVul
from dongtai_common.models.user import User
from dongtai_common.models.vulnerablity import IastVulnerabilityModel
from dongtai_common.utils.settings import get_managed


class MessageTypeChoices(IntegerChoices):
    CHANGE_STATUS = 1
    VUL_RECHECK = 2
    PUSH_TO_INTEGRATION = 3
    VUL_FOUND = 4


class IastVulLog(models.Model):
    msg_type = models.IntegerField()
    msg = models.TextField()
    meta_data = models.JSONField()
    datetime = models.IntegerField(default=lambda: int(time()))
    vul = models.ForeignKey(
        IastVulnerabilityModel, models.DO_NOTHING, default=-1, db_constraint=False
    )
    asset_vul = models.ForeignKey(
        IastAssetVul, models.DO_NOTHING, default=-1, db_constraint=False
    )
    user = models.ForeignKey(User, models.DO_NOTHING, db_constraint=False)

    class Meta:
        managed = get_managed()
        db_table = "iast_vul_log"
