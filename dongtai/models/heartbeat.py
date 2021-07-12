#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/5/22 18:21
# software: PyCharm
# project: dongtai-models

from django.db import models
from django.utils.translation import gettext_lazy as _

from dongtai.models.agent import IastAgent


class Heartbeat(models.Model):
    hostname = models.CharField(max_length=1000, blank=True, null=True)
    network = models.CharField(max_length=2000, blank=True, null=True)
    memory = models.CharField(max_length=1000, blank=True, null=True)
    cpu = models.CharField(max_length=1000, blank=True, null=True)
    disk = models.CharField(max_length=1000, blank=True, null=True)
    pid = models.CharField(max_length=1050, blank=True, null=True)
    env = models.TextField(blank=True, null=True)
    req_count = models.IntegerField(blank=True, null=True)
    dt = models.IntegerField(blank=True, null=True)
    agent = models.ForeignKey(
        to=IastAgent,
        on_delete=models.DO_NOTHING,
        related_name='heartbeats',
        related_query_name='heartbeat',
        verbose_name=_('agent'),
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'iast_heartbeat'
