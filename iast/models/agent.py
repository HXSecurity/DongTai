#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/30 下午5:29
# software: PyCharm
# project: lingzhi-webapi
from django.db import models
from django.utils.translation import gettext_lazy as _

from iast.models import User
from iast.models.server import IastServerModel


class IastAgent(models.Model):
    token = models.CharField(max_length=255, blank=True, null=True)
    version = models.CharField(max_length=255, blank=True, null=True)
    latest_time = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(User, models.DO_NOTHING)
    server = models.ForeignKey(
        to=IastServerModel,
        on_delete=models.DO_NOTHING,
        related_name='agents',
        related_query_name='agent',
        verbose_name=_('server'),
    )
    is_running = models.IntegerField(blank=True, null=True)
    control = models.IntegerField(blank=True, null=True)
    is_control = models.IntegerField(blank=True, null=True)
    # fixme 将bind_project_id更改为project与agent的关联表
    bind_project_id = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        managed = False
        db_table = 'iast_agent'
