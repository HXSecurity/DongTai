#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/30 下午5:29
# software: PyCharm
# project: dongtai-models
from django.db import models
from django.utils.translation import gettext_lazy as _

from dongtai_common.models import User

from dongtai_common.models.server import IastServer
from dongtai_common.utils.settings import get_managed
from dongtai_common.models.project import IastProject
from dongtai_common.models.project_version import IastProjectVersion

from _typeshed import Incomplete
class IastAgent(models.Model):
    token: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    version: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    latest_time: Incomplete = models.IntegerField(blank=True, null=True)
    user: Incomplete = models.ForeignKey(User, models.DO_NOTHING)
    server: Incomplete = models.ForeignKey(
        to=IastServer,
        on_delete=models.DO_NOTHING,
        related_name='agents',
        null=True,
        related_query_name='agent',
        verbose_name=_('server'),
    )
    is_audit: Incomplete = models.IntegerField(blank=True, null=True)
    is_running: Incomplete = models.IntegerField(blank=True, null=True)
    is_core_running: Incomplete = models.IntegerField(blank=True, null=True)
    control: Incomplete = models.IntegerField(blank=True, null=True)
    is_control: Incomplete = models.IntegerField(blank=True, null=True)
    bind_project: Incomplete = models.ForeignKey(IastProject,
                                     on_delete=models.DO_NOTHING,
                                     blank=True,
                                     null=True,
                                     default=-1)
    project_version: Incomplete = models.ForeignKey(IastProjectVersion,
                                     on_delete=models.DO_NOTHING,
                                     blank=True,
                                     null=True,
                                     default=-1)
    project_name: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    online: Incomplete = models.PositiveSmallIntegerField(blank=True, default=0)
    language: Incomplete = models.CharField(max_length=10, blank=True, null=True)
    filepathsimhash: Incomplete = models.CharField(max_length=255,
                                       default='',
                                       blank=True,
                                       null=True)
    servicetype: Incomplete = models.CharField(max_length=255,
                                   default='',
                                   blank=True,
                                   null=True)
    alias: Incomplete = models.CharField(default='', max_length=255, blank=True, null=True)
    startup_time: Incomplete = models.IntegerField(default=0, null=False)
    register_time: Incomplete = models.IntegerField(default=0, null=False)
    actual_running_status: Incomplete = models.IntegerField(default=1, null=False)
    except_running_status: Incomplete = models.IntegerField(default=1, null=False)
    state_status: Incomplete = models.IntegerField(default=1, null=False)


    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'iast_agent'
