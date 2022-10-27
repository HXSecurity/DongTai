#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/5/25 14:47
# software: PyCharm
# project: dongtai-models
from django.db import models
from dongtai_common.utils.settings import get_managed


from _typeshed import Incomplete
class IastServer(models.Model):
    hostname: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    ip: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    port: Incomplete = models.IntegerField(blank=True, null=True)
    environment: Incomplete = models.TextField(blank=True, null=True)
    path: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    status: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    container: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    container_path: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    cluster_name: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    cluster_version: Incomplete = models.CharField(max_length=100, blank=True, null=True)
    command: Incomplete = models.TextField(blank=True, null=True)
    env: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    runtime: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    create_time: Incomplete = models.IntegerField(blank=True, null=True)
    update_time: Incomplete = models.IntegerField(blank=True, null=True)
    network: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    protocol: Incomplete = models.CharField(max_length=255,
                                blank=True,
                                null=True,
                                default='')
    pid: Incomplete = models.IntegerField(blank=True, null=True)

    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'iast_server'
