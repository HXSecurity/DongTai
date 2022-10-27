#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/5/22 18:21
# software: PyCharm
# project: dongtai-models
from django.db import models

from dongtai_common.models.agent import IastAgent
from dongtai_common.utils.settings import get_managed


from _typeshed import Incomplete
class IastErrorlog(models.Model):
    errorlog: Incomplete = models.TextField(blank=True, null=True)
    state: Incomplete = models.CharField(max_length=50, blank=True, null=True)
    dt: Incomplete = models.IntegerField(blank=True, null=True)
    agent: Incomplete = models.ForeignKey(IastAgent, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'iast_errorlog'
