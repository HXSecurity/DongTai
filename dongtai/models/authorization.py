#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/5/25 14:48
# software: PyCharm
# project: dongtai-models
from django.db import models
import os


class IastAuthorization(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    token = models.CharField(max_length=50, blank=True, null=True)
    view_name = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=20, blank=True, null=True)
    dt = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True if os.getenv('environment',None) == 'TEST' else False
        db_table = 'iast_authorization'
