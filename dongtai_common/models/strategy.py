from django.db import models

from dongtai_common.models import User
from dongtai_common.models.hook_type import HookType
from dongtai_common.models.vul_level import IastVulLevel
from dongtai_common.utils.settings import get_managed
from time import time


class IastStrategyModel(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    vul_type = models.CharField(max_length=255, blank=True, null=True)
    level = models.ForeignKey(IastVulLevel, models.DO_NOTHING, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    dt = models.IntegerField(blank=True, null=True, default=time)
    vul_name = models.CharField(max_length=255, blank=True, null=True)
    vul_desc = models.TextField(blank=True, null=True)
    vul_fix = models.TextField(blank=True, null=True)
    hook_type = models.ForeignKey(HookType,
                                  models.DO_NOTHING,
                                  blank=True,
                                  null=True)
    system_type = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        managed = get_managed()
        db_table = 'iast_strategy'
