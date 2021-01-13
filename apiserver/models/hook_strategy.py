#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/13 下午7:14
# software: PyCharm
# project: lingzhi-agent-server
from django.db import models


class IastHookStrategy(models.Model):
    value = models.CharField(max_length=255, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    target = models.CharField(max_length=255, blank=True, null=True)
    inherit = models.CharField(max_length=255, blank=True, null=True)
    track = models.CharField(max_length=5, blank=True, null=True)
    create_time = models.IntegerField(blank=True, null=True)
    update_time = models.IntegerField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'iast_hook_strategy'
