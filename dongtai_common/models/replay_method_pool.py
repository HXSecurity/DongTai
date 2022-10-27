#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/7/3 下午2:34
# project: dongtai-engine

from django.db import models

from dongtai_common.models.agent import IastAgent
from dongtai_common.utils.settings import get_managed


from _typeshed import Incomplete
class IastAgentMethodPoolReplay(models.Model):
    agent: Incomplete = models.ForeignKey(IastAgent, models.DO_NOTHING, blank=True, null=True)
    url: Incomplete = models.CharField(max_length=2000, blank=True, null=True)
    uri: Incomplete = models.CharField(max_length=2000, blank=True, null=True)
    http_method: Incomplete = models.CharField(max_length=10, blank=True, null=True)
    http_scheme: Incomplete = models.CharField(max_length=20, blank=True, null=True)
    http_protocol: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    req_header: Incomplete = models.CharField(max_length=2000, blank=True, null=True)
    req_params: Incomplete = models.CharField(max_length=2000, blank=True, null=True)
    req_data: Incomplete = models.CharField(max_length=4000, blank=True, null=True)
    res_header: Incomplete = models.CharField(max_length=1000, blank=True, null=True)
    res_body: Incomplete = models.CharField(max_length=1000, blank=True, null=True)
    context_path: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    method_pool: Incomplete = models.TextField(blank=True, null=True)  # This field type is a guess.
    clent_ip: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    create_time: Incomplete = models.IntegerField(blank=True, null=True)
    update_time: Incomplete = models.IntegerField(blank=True, null=True)
    replay_id: Incomplete = models.IntegerField(blank=True, null=True)
    replay_type: Incomplete = models.IntegerField(blank=True, null=True)
    relation_id: Incomplete = models.IntegerField(blank=True, null=True)

    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'iast_agent_method_pool_replay'
