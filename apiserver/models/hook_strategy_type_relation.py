#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/13 下午7:15
# software: PyCharm
# project: lingzhi-agent-server
from django.db import models

from apiserver.models.hook_strategy import IastHookStrategy
from apiserver.models.hook_strategy_type import IastHookStrategyType


class IastHookStrategyTypeRelation(models.Model):
    strategy = models.ForeignKey(IastHookStrategy, models.DO_NOTHING, blank=True, null=True)
    type = models.ForeignKey(IastHookStrategyType, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'iast_hook_strategy_type_relation'
