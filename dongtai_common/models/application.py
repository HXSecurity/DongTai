#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/5/25 14:47
# software: PyCharm
# project: dongtai-models
from django.db import models
from dongtai_common.utils.settings import get_managed

from dongtai_common.models import User


class IastApplicationModel(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    path = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    server_id = models.IntegerField(blank=True, null=True)
    vul_count = models.IntegerField(blank=True, null=True)
    dt = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = get_managed()
        db_table = "iast_application"
        unique_together = (("name", "path"),)
