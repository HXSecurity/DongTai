#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/30 下午5:32
# software: PyCharm
# project: dongtai-models
from django.db import models

from dongtai.models import User
from dongtai.models.strategy_user import IastStrategyUser
import os
from dongtai.utils.customfields import trans_char_field


class IastProject(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    mode = trans_char_field(['插桩模式', '流量模式'])(max_length=255,
                                              blank=True,
                                              null=True)
    vul_count = models.PositiveIntegerField(blank=True, null=True)
    agent_count = models.IntegerField(blank=True, null=True)
    latest_time = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    # openapi服务不必使用该字段
    scan = models.ForeignKey(IastStrategyUser,
                             models.DO_NOTHING,
                             blank=True,
                             null=True)

    class Meta:
        managed = True if os.getenv('environment', None) == 'TEST' else False
        db_table = 'iast_project'
