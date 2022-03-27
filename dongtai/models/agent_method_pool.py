#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/14 下午3:35
# software: PyCharm
# project: dongtai-models
from django.db import models
from django.utils.translation import gettext_lazy as _

from dongtai.models.agent import IastAgent
from dongtai.models.hook_strategy import HookStrategy
from dongtai.utils.settings import get_managed


class MethodPool(models.Model):
    agent = models.ForeignKey(IastAgent,
                              models.DO_NOTHING,
                              blank=True,
                              null=True,
                              db_constraint=False)
    url = models.CharField(max_length=2000, blank=True, null=True)
    uri = models.CharField(max_length=2000, blank=True, null=True)
    http_method = models.CharField(max_length=10, blank=True, default='')
    http_scheme = models.CharField(max_length=20, blank=True, null=True)
    http_protocol = models.CharField(max_length=255, blank=True, null=True)
    req_header = models.CharField(max_length=2000, blank=True, null=True)
    req_params = models.CharField(max_length=2000, blank=True, null=True)
    req_data = models.CharField(max_length=4000, blank=True, null=True)
    res_header = models.CharField(max_length=1000, blank=True, null=True)
    res_body = models.TextField( blank=True, null=True)
    req_header_fs = models.TextField(blank=True,
                                     null=True,
                                     db_column='req_header_for_search')
    context_path = models.CharField(max_length=255, blank=True, null=True)
    method_pool = models.TextField(blank=True,
                                   null=True)  # This field type is a guess.
    pool_sign = models.CharField(unique=True,
                                 max_length=40,
                                 blank=True,
                                 null=True)  # This field type is a guess.
    clent_ip = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.IntegerField(blank=True, null=True)
    update_time = models.IntegerField(blank=True, null=True)
    uri_sha1 = models.CharField(max_length=40,
                                blank=True,
                                default='',
                                db_index=True)
    sinks = models.ManyToManyField(
        HookStrategy,
        verbose_name=_('sinks'),
        blank=True,
        related_name="method_pools",
        related_query_name="method_pool",
    )

    class Meta:
        managed = get_managed()
        db_table = 'iast_agent_method_pool'
        indexes = [models.Index(fields=['uri_sha1', 'http_method', 'agent'])]
