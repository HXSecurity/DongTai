#!/usr/bin/env python
# datetime:2021/1/13 下午6:38
from time import time

from django.db import models

from dongtai_common.models.program_language import IastProgramLanguage
from dongtai_common.utils.settings import get_managed
from dongtai_common.utils.db import get_timestamp


class HookType(models.Model):
    type = models.IntegerField()
    name = models.CharField(max_length=255, blank=True)
    value = models.CharField(max_length=255, blank=True)
    enable = models.IntegerField(blank=True)
    create_time = models.IntegerField(blank=True, null=True, default=get_timestamp)
    update_time = models.IntegerField(blank=True, null=True, default=get_timestamp)
    created_by = models.IntegerField(blank=True)
    language = models.ForeignKey(
        IastProgramLanguage,
        blank=True,
        on_delete=models.DO_NOTHING,
        db_constraint=False,
    )
    vul_strategy = models.ForeignKey(
        "dongtai_common.IastStrategyModel",
        blank=True,
        default=-1,
        null=True,
        on_delete=models.DO_NOTHING,
        db_column="strategy_id",
        db_constraint=False,
    )
    system_type = models.IntegerField(blank=True, default=0)

    class Meta:
        managed = get_managed()
        db_table = "iast_hook_type"
