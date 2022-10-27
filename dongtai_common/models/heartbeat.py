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


from _typeshed import Incomplete
class IastHeartbeat(models.Model):
    memory: Incomplete = models.CharField(max_length=1000, blank=True, null=True)
    cpu: Incomplete = models.CharField(max_length=1000, blank=True, null=True)
    disk: Incomplete = models.CharField(max_length=1000, blank=True, null=True)
    req_count: Incomplete = models.IntegerField(blank=True, null=True)
    dt: Incomplete = models.IntegerField(blank=True, null=True)
    report_queue: Incomplete = models.PositiveIntegerField(default=0,
                                               null=False,
                                               blank=False)
    method_queue: Incomplete = models.PositiveIntegerField(default=0,
                                               null=False,
                                               blank=False)
    replay_queue: Incomplete = models.PositiveIntegerField(default=0,
                                               null=False,
                                               blank=False)

    agent: Incomplete = models.ForeignKey(
        to=IastAgent,
        on_delete=models.DO_NOTHING,
        related_name='heartbeats',
        related_query_name='heartbeat',
        verbose_name=_('agent'),
        blank=True,
        null=True
    )

    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'iast_heartbeat'
