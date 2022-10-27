from django.db import models

from dongtai_common.models.agent import IastAgent
from dongtai_common.utils.settings import get_managed
from django.db.models import IntegerChoices
from dongtai_common.models.user import User
from dongtai_common.models.asset import Asset
from dongtai_common.models.vulnerablity import IastVulnerabilityModel
from time import time
from dongtai_common.models.asset_vul import IastAssetVul, IastVulAssetRelation


from _typeshed import Incomplete
class MessageTypeChoices(IntegerChoices):
    CHANGE_STATUS: int = 1
    VUL_RECHECK: int = 2
    PUSH_TO_INTEGRATION: int = 3
    VUL_FOUND: int = 4


class IastVulLog(models.Model):
    msg_type: Incomplete = models.IntegerField(blank=True, null=True)
    msg: Incomplete = models.TextField(blank=True, null=True)
    meta_data: Incomplete = models.JSONField(blank=True, null=True)
    datetime: Incomplete = models.IntegerField(blank=True, null=True, default=time)
    vul: Incomplete = models.ForeignKey(IastVulnerabilityModel,
                                models.DO_NOTHING,
                                default=-1,
                                db_constraint=False)
    asset_vul: Incomplete = models.ForeignKey(IastAssetVul,
                                      models.DO_NOTHING,
                                      default=-1,
                                      db_constraint=False)
    user: Incomplete = models.ForeignKey(User, models.DO_NOTHING, db_constraint=False)

    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'iast_vul_log'
