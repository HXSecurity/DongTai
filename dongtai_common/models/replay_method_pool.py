#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/7/3 下午2:34
# project: dongtai-engine

from django.db import models

from dongtai_common.models.agent import IastAgent
from dongtai_common.utils.settings import get_managed


class IastAgentMethodPoolReplay(models.Model):
    agent = models.ForeignKey(IastAgent, models.DO_NOTHING, blank=True, null=True)
    url = models.CharField(max_length=2000, blank=True, null=True)
    uri = models.CharField(max_length=2000, blank=True, null=True)
    http_method = models.CharField(max_length=10, blank=True, null=True)
    http_scheme = models.CharField(max_length=20, blank=True, null=True)
    http_protocol = models.CharField(max_length=255, blank=True, null=True)
    req_header = models.CharField(max_length=2000, blank=True, null=True)
    req_params = models.CharField(max_length=2000, blank=True, null=True)
    req_data = models.CharField(max_length=4000, blank=True, null=True)
    res_header = models.CharField(max_length=1000, blank=True, null=True)
    res_body = models.CharField(max_length=1000, blank=True, null=True)
    context_path = models.CharField(max_length=255, blank=True, null=True)
    method_pool = models.TextField(blank=True, null=True)  # This field type is a guess.
    clent_ip = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.IntegerField(blank=True, null=True)
    update_time = models.IntegerField(blank=True, null=True)
    replay_id = models.IntegerField(blank=True, null=True)
    replay_type = models.IntegerField(blank=True, null=True)
    relation_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = get_managed()
        db_table = 'iast_agent_method_pool_replay'
