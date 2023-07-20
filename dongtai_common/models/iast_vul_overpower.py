#!/usr/bin/env python
# datetime:2020/10/31 11:38
from django.db import models

from dongtai_common.models.agent import IastAgent

from dongtai_common.utils.settings import get_managed


class IastVulOverpower(models.Model):
    agent = models.ForeignKey(IastAgent, models.DO_NOTHING, blank=True, null=True)
    http_url = models.CharField(max_length=2000, blank=True, null=True)
    http_uri = models.CharField(max_length=2000, blank=True, null=True)
    http_query_string = models.CharField(max_length=2000, blank=True, null=True)
    http_method = models.CharField(max_length=10, blank=True, null=True)
    http_scheme = models.CharField(max_length=255, blank=True, null=True)
    http_protocol = models.CharField(max_length=255, blank=True, null=True)
    http_header = models.CharField(max_length=2000, blank=True, null=True)
    x_trace_id = models.CharField(max_length=255, blank=True, null=True)
    cookie = models.CharField(max_length=2000, blank=True, null=True)
    sql = models.CharField(max_length=2000, blank=True, null=True)
    created_time = models.DateTimeField(blank=True, null=True)
    updated_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = get_managed()
        db_table = "iast_vul_overpower"
