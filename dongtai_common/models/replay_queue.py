#!/usr/bin/env python
# -*- coding:utf-8 -*-
# datetime: 2021/7/1 下午3:02
from django.db import models

from dongtai_common.models.agent import IastAgent
from dongtai_common.utils.settings import get_managed
from dongtai_common.models.vul_recheck_payload import IastVulRecheckPayload


class IastReplayQueue(models.Model):
    agent = models.ForeignKey(IastAgent, models.DO_NOTHING, blank=True, null=True)
    relation_id = models.IntegerField(blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    result = models.IntegerField(blank=True, null=True)
    create_time = models.IntegerField(blank=True, null=True)
    update_time = models.IntegerField(blank=True, null=True)
    verify_time = models.IntegerField(blank=True, null=True)
    uri = models.CharField(max_length=2000, blank=True, null=True)
    method = models.CharField(max_length=10, blank=True, null=True)
    scheme = models.CharField(max_length=10, blank=True, null=True)
    header = models.CharField(max_length=4000, blank=True, null=True)
    params = models.CharField(max_length=2000, blank=True, null=True)
    body = models.CharField(max_length=4000, blank=True, null=True)
    replay_type = models.IntegerField(blank=True, null=True)
    payload = models.ForeignKey(
        IastVulRecheckPayload, models.DO_NOTHING, blank=True, null=True, default=-1
    )

    class Meta:
        managed = get_managed()
        db_table = "iast_replay_queue"
        ordering = ("-replay_type",)
