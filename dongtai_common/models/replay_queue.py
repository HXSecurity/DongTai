#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/7/1 下午3:02
# project: dongtai-engine
from django.db import models

from dongtai_common.models.agent import IastAgent
from dongtai_common.models.vulnerablity import IastVulnerabilityModel
from dongtai_common.utils.settings import get_managed
from dongtai_common.models.vul_recheck_payload import IastVulRecheckPayload

from _typeshed import Incomplete
class IastReplayQueue(models.Model):
    agent: Incomplete = models.ForeignKey(IastAgent, models.DO_NOTHING, blank=True, null=True)
    relation_id: Incomplete = models.IntegerField(blank=True, null=True)
    state: Incomplete = models.IntegerField(blank=True, null=True)
    count: Incomplete = models.IntegerField(blank=True, null=True)
    result: Incomplete = models.IntegerField(blank=True, null=True)
    create_time: Incomplete = models.IntegerField(blank=True, null=True)
    update_time: Incomplete = models.IntegerField(blank=True, null=True)
    verify_time: Incomplete = models.IntegerField(blank=True, null=True)
    uri: Incomplete = models.CharField(max_length=2000, blank=True, null=True)
    method: Incomplete = models.CharField(max_length=10, blank=True, null=True)
    scheme: Incomplete = models.CharField(max_length=10, blank=True, null=True)
    header: Incomplete = models.CharField(max_length=4000, blank=True, null=True)
    params: Incomplete = models.CharField(max_length=2000, blank=True, null=True)
    body: Incomplete = models.CharField(max_length=4000, blank=True, null=True)
    replay_type: Incomplete = models.IntegerField(blank=True, null=True)
    payload: Incomplete = models.ForeignKey(IastVulRecheckPayload,
                                models.DO_NOTHING,
                                blank=True,
                                null=True,
                                default=-1)

    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'iast_replay_queue'
        ordering: Incomplete = ('-replay_type',)
