#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/5/22 18:21
# software: PyCharm
# project: webapi

from django.db import models

from apiserver.models.agent import IastAgent
from user.models import User


class IastHeartbeat(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    hostname = models.CharField(max_length=1000, blank=True, null=True)
    network = models.CharField(max_length=2000, blank=True, null=True)
    memory = models.CharField(max_length=1000, blank=True, null=True)
    cpu = models.CharField(max_length=1000, blank=True, null=True)
    disk = models.CharField(max_length=1000, blank=True, null=True)
    pid = models.CharField(max_length=1050, blank=True, null=True)
    env = models.TextField(blank=True, null=True)
    req_count = models.IntegerField(blank=True, null=True)
    dt = models.IntegerField(blank=True, null=True)
    agent = models.ForeignKey(IastAgent, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'iast_heartbeat'
