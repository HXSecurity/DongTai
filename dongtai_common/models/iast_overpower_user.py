#!/usr/bin/env python
# datetime:2020/10/30 15:46
from django.db import models
from dongtai_common.utils.settings import get_managed


class IastOverpowerUserAuth(models.Model):
    server_name = models.CharField(max_length=255, blank=True, null=True)
    server_port = models.CharField(max_length=5, blank=True, null=True)
    app_name = models.CharField(max_length=50, blank=True, null=True)
    http_url = models.CharField(max_length=255, blank=True, null=True)
    http_query_string = models.CharField(max_length=2000, blank=True, null=True)
    auth_sql = models.CharField(max_length=255, blank=True, null=True)
    auth_value = models.CharField(max_length=1000, blank=True, null=True)
    jdbc_class = models.CharField(max_length=255, blank=True, null=True)
    created_time = models.DateTimeField(blank=True, null=True)
    updated_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = get_managed()
        db_table = "iast_user_auth"
