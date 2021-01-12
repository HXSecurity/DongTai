#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/30 下午5:29
# software: PyCharm
# project: lingzhi-webapi
from django.db import models

from apiserver.models.server import IastServerModel
from user.models import User


class IastAgent(models.Model):
    token = models.CharField(max_length=255, blank=True, null=True)
    version = models.CharField(max_length=255, blank=True, null=True)
    latest_time = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(User, models.DO_NOTHING)
    server = models.ForeignKey(IastServerModel, models.DO_NOTHING)
    is_running = models.IntegerField(blank=True, null=True)
    control = models.IntegerField(blank=True, null=True)
    is_control = models.IntegerField(blank=True, null=True)
    bind_project_id = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        managed = False
        db_table = 'iast_agent'
