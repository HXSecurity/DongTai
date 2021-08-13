#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/5/22 18:21
# software: PyCharm
# project: dongtai-models
from django.db import models

from dongtai.models.agent import IastAgent
import os


class IastErrorlog(models.Model):
    errorlog = models.TextField(blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    dt = models.IntegerField(blank=True, null=True)
    agent = models.ForeignKey(IastAgent, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True if os.getenv('environment',None) == 'TEST' else False
        db_table = 'iast_errorlog'
