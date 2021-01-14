#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/14 下午3:35
# software: PyCharm
# project: lingzhi-agent-server
from django.db import models

from apiserver.models.agent import IastAgent


class IastAgentMethodPool(models.Model):
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
    language = models.CharField(max_length=20, blank=True, null=True)
    method_pool = models.TextField(blank=True, null=True)  # This field type is a guess.
    pool_sign = models.CharField(unique=True, max_length=32, blank=True, null=True)  # This field type is a guess.
    clent_ip = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.IntegerField(blank=True, null=True)
    update_time = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'iast_agent_method_pool'
