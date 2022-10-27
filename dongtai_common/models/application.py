#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/5/25 14:47
# software: PyCharm
# project: dongtai-models
from django.db import models
from dongtai_common.utils.settings import get_managed

from dongtai_common.models import User


from _typeshed import Incomplete
class IastApplicationModel(models.Model):
    user: Incomplete = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    name: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    path: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    status: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    server_id: Incomplete = models.IntegerField(blank=True, null=True)
    vul_count: Incomplete = models.IntegerField(blank=True, null=True)
    dt: Incomplete = models.IntegerField(blank=True, null=True)

    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'iast_application'
        unique_together: Incomplete = (('name', 'path'),)
