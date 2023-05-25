#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/5/22 18:21
# software: PyCharm
# project: dongtai-models

from django.db import models
from django.utils.translation import gettext_lazy as _

from dongtai_common.models.agent import IastAgent
from dongtai_common.utils.settings import get_managed


class IastHeartbeat(models.Model):
    memory = models.CharField(max_length=1000, blank=True, null=True)
    cpu = models.CharField(max_length=1000, blank=True, null=True)
    disk = models.CharField(max_length=1000, blank=True, null=True)
    req_count = models.IntegerField(default=0, blank=True, null=True)
    dt = models.IntegerField(blank=True, null=True)
    report_queue = models.PositiveIntegerField(default=0,
                                               null=False,
                                               blank=False)
    method_queue = models.PositiveIntegerField(default=0,
                                               null=False,
                                               blank=False)
    replay_queue = models.PositiveIntegerField(default=0,
                                               null=False,
                                               blank=False)

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
        managed = get_managed()
        db_table = 'iast_heartbeat'
