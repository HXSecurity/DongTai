#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/5/25 14:47
# software: PyCharm
# project: dongtai-models
from django.db import models
from dongtai_common.utils.settings import get_managed


class IastServer(models.Model):
    hostname = models.CharField(max_length=255, blank=True, null=True)
    ip = models.CharField(max_length=255, blank=True, null=True)
    port = models.IntegerField(blank=True, null=True)
    environment = models.TextField(blank=True, null=True)
    path = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    container = models.CharField(max_length=255, blank=True, null=True)
    container_path = models.CharField(max_length=255, blank=True, null=True)
    cluster_name = models.CharField(max_length=255, blank=True, null=True)
    cluster_version = models.CharField(max_length=100, blank=True, null=True)
    command = models.TextField(blank=True, null=True)
    env = models.CharField(max_length=255, blank=True, null=True)
    runtime = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.IntegerField(blank=True, null=True)
    update_time = models.IntegerField(blank=True, null=True)
    network = models.CharField(max_length=255, blank=True, null=True)
    protocol = models.CharField(max_length=255,
                                blank=True,
                                null=True,
                                default='')
    pid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = get_managed()
        db_table = 'iast_server'
