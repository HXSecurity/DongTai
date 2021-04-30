#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/4/30 下午12:08
# project: dongtai-webapi
from django.db import models


class ScaRecord(models.Model):
    page = models.IntegerField(blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    dt = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    data = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sca_record'
