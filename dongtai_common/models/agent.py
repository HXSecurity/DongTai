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
import json
from dongtai_common.models.department import Department
from time import time


class IastAgent(models.Model):
    token = models.CharField(max_length=255, blank=True, null=True)
    version = models.CharField(max_length=255, blank=True, null=True)
    latest_time = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(User, models.DO_NOTHING)
    server = models.ForeignKey(
        to=IastServer,
        on_delete=models.DO_NOTHING,
        related_name='agents',
        null=True,
        related_query_name='agent',
        verbose_name=_('server'),
    )
    is_audit = models.IntegerField(blank=True, null=True)
    is_running = models.IntegerField(blank=True, null=True)
    is_core_running = models.IntegerField(blank=True, null=True)
    control = models.IntegerField(blank=True, null=True)
    is_control = models.IntegerField(blank=True, null=True)
    bind_project = models.ForeignKey(IastProject,
                                     on_delete=models.CASCADE,
                                     blank=True,
                                     null=True,
                                     default=-1)
    project_version = models.ForeignKey(IastProjectVersion,
                                        on_delete=models.CASCADE,
                                        blank=True,
                                        null=True,
                                        default=-1)
    project_name = models.CharField(max_length=255, blank=True, null=True)
    online = models.PositiveSmallIntegerField(blank=True, default=0)
    language = models.CharField(max_length=10, blank=True, null=True)
    filepathsimhash = models.CharField(max_length=255,
                                       default='',
                                       blank=True,
                                       null=True)
    servicetype = models.CharField(max_length=255,
                                   default='',
                                   blank=True,
                                   null=True)
    alias = models.CharField(default='', max_length=255, blank=True, null=True)
    startup_time = models.IntegerField(default=0, null=False)
    register_time = models.IntegerField(default=0, null=False)
    actual_running_status = models.IntegerField(default=1, null=False)
    except_running_status = models.IntegerField(default=1, null=False)
    state_status = models.IntegerField(default=1, null=False)
    events = models.JSONField(null=False, default=lambda: ['注册成功'])
    department = models.ForeignKey(Department,
                                   models.DO_NOTHING,
                                   blank=True,
                                   null=True)
    allow_report = models.IntegerField(default=1, null=False)

    class Meta:
        managed = get_managed()
        db_table = 'iast_agent'

    def append_events(self, event: str):
        self.update_events_if_need()
        events_list = self.events if self.events else ["注册成功"]
        events_list.append(event)
        self.events = events_list
        self.save()
        IastAgentEvent.objects.create(agent_id=self.id, name=event)

    def only_register(self):
        events_list = self.events if self.events else ["注册成功"]
        return events_list == ['注册成功']

    def update_events(self):
        for event in self.events:
            IastAgentEvent.objects.create(agent_id=self.id,
                                          name=event,
                                          time=None)

    def is_need_to_update(self):
        if self.events and len(self.events) <= self.new_events.count():
            return False
        return True

    def update_events_if_need(self):
        if self.is_need_to_update():
            self.update_events()


class IastAgentEvent(models.Model):
    agent = models.ForeignKey(IastAgent,
                              on_delete=models.CASCADE,
                              related_name='new_events',
                              null=True)
    name = models.CharField(default='', max_length=255, blank=True, null=True)
    time = models.IntegerField(default=lambda: int(time()),
                               blank=True,
                               null=True)

    class Meta:
        managed = get_managed()
        db_table = 'iast_agent_event'


# class IastAgent(models.Model):
#
#    class Meta:
#        managed = get_managed()
#        db_table = 'iast_agent'
