#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/10/31 11:38
# software: PyCharm
# project: dongtai-models
from django.db import models

from dongtai_common.models.agent import IastAgent

from dongtai_common.utils.settings import get_managed


from _typeshed import Incomplete
class IastVulOverpower(models.Model):
    agent: Incomplete = models.ForeignKey(IastAgent, models.DO_NOTHING, blank=True, null=True)
    http_url: Incomplete = models.CharField(max_length=2000, blank=True, null=True)
    http_uri: Incomplete = models.CharField(max_length=2000, blank=True, null=True)
    http_query_string: Incomplete = models.CharField(max_length=2000, blank=True, null=True)
    http_method: Incomplete = models.CharField(max_length=10, blank=True, null=True)
    http_scheme: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    http_protocol: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    http_header: Incomplete = models.CharField(max_length=2000, blank=True, null=True)
    x_trace_id: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    cookie: Incomplete = models.CharField(max_length=2000, blank=True, null=True)
    sql: Incomplete = models.CharField(max_length=2000, blank=True, null=True)
    created_time: Incomplete = models.DateTimeField(blank=True, null=True)
    updated_time: Incomplete = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'iast_vul_overpower'
