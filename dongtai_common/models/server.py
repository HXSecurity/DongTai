#!/usr/bin/env python
# -*- coding:utf-8 -*-
# datetime:2020/5/25 14:47
from django.db import models
from dongtai_common.utils.settings import get_managed


class IastServer(models.Model):
    hostname = models.CharField(max_length=255, blank=True)
    ip = models.CharField(max_length=255, blank=True)
    port = models.IntegerField()
    environment = models.TextField(blank=True, null=True)
    path = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=255, blank=True)
    container = models.CharField(max_length=255, blank=True)
    container_path = models.CharField(max_length=255, blank=True)
    cluster_name = models.CharField(max_length=255, blank=True)
    cluster_version = models.CharField(max_length=100, blank=True)
    command = models.TextField(blank=True)
    env = models.CharField(max_length=255, blank=True)
    runtime = models.CharField(max_length=255, blank=True)
    create_time = models.IntegerField()
    update_time = models.IntegerField()
    network = models.CharField(max_length=255, blank=True)
    protocol = models.CharField(max_length=255, blank=True)
    pid = models.IntegerField(blank=True)
    ipaddresslist = models.JSONField(null=False, default=list)

    class Meta:
        managed = get_managed()
        db_table = "iast_server"
