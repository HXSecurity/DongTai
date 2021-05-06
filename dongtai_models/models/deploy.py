#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/6/3 11:36
# software: PyCharm
# project: dongtai-models

from django.db import models


class IastDeployDesc(models.Model):
    desc = models.TextField(blank=True, null=True)
    middleware = models.CharField(max_length=255, blank=True, null=True)
    os = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'iast_deploy'
