#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/13 下午7:26
# software: PyCharm
# project: dongtai-models
from django.db import models

from dongtai_models.models.talent import Talent


class IastHookTalentStrategy(models.Model):
    talent = models.ForeignKey(Talent, models.DO_NOTHING, blank=True, null=True)
    values = models.CharField(max_length=500, blank=True, null=True)
    create_time = models.IntegerField(blank=True, null=True)
    update_time = models.IntegerField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'iast_hook_talent_strategy'
