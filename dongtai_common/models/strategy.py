from django.db import models

from dongtai_common.models import User
from dongtai_common.models.hook_type import HookType
from dongtai_common.models.vul_level import IastVulLevel
from dongtai_common.utils.settings import get_managed
from time import time

from _typeshed import Incomplete
class IastStrategyModel(models.Model):
    user: Incomplete = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    vul_type: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    level: Incomplete = models.ForeignKey(IastVulLevel, models.DO_NOTHING, blank=True, null=True)
    state: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    dt: Incomplete = models.IntegerField(blank=True, null=True, default=time)
    vul_name: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    vul_desc: Incomplete = models.TextField(blank=True, null=True)
    vul_fix: Incomplete = models.TextField(blank=True, null=True)
    hook_type: Incomplete = models.ForeignKey(HookType,
                                  models.DO_NOTHING,
                                  blank=True,
                                  null=True)
    system_type: Incomplete = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'iast_strategy'
