#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/10/30 15:46
# software: PyCharm
# project: dongtai-models
from django.db import models
from dongtai_common.utils.settings import get_managed



from _typeshed import Incomplete
class IastOverpowerUserAuth(models.Model):
    server_name: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    server_port: Incomplete = models.CharField(max_length=5, blank=True, null=True)
    app_name: Incomplete = models.CharField(max_length=50, blank=True, null=True)
    http_url: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    http_query_string: Incomplete = models.CharField(max_length=2000, blank=True, null=True)
    auth_sql: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    auth_value: Incomplete = models.CharField(max_length=1000, blank=True, null=True)
    jdbc_class: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    created_time: Incomplete = models.DateTimeField(blank=True, null=True)
    updated_time: Incomplete = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'iast_user_auth'
