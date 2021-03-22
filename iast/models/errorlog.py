#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/5/22 18:21
# software: PyCharm
# project: webapi
from django.db import models
from django.utils.translation import gettext_lazy as _

from iast.models.agent import IastAgent


class Errorlog(models.Model):
    errorlog = models.TextField(blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    dt = models.IntegerField(blank=True, null=True)
    agent = models.ForeignKey(
        to=IastAgent,
        on_delete=models.DO_NOTHING,
        related_name='error_logs',
        related_query_name='error_log',
        verbose_name=_('agent'),
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'iast_errorlog'
