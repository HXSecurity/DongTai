#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/5/22 18:21
# software: PyCharm
# project: webapi
from django.db import models

from apiserver.models.agent import IastAgent
from user.models import User


class IastErrorlog(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    errorlog = models.TextField(blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    dt = models.IntegerField(blank=True, null=True)
    agent = models.ForeignKey(IastAgent, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'iast_errorlog'
