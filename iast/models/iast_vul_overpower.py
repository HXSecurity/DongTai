#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/10/31 11:38
# software: PyCharm
# project: webapi
from django.db import models
from django.utils.translation import gettext_lazy as _

from iast.models import User
from iast.models.agent import IastAgent


class VulOverpower(models.Model):
    agent = models.ForeignKey(
        to=IastAgent,
        on_delete=models.DO_NOTHING,
        related_name='vul_overpowers',
        related_query_name='vul_overpower',
        verbose_name=_('agent'),
        blank=True,
        null=True
    )
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
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    created_time = models.DateTimeField(blank=True, null=True)
    updated_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'iast_vul_overpower'
