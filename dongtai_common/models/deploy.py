#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/6/3 11:36
# software: PyCharm
# project: dongtai-models

from django.db import models
from dongtai_common.utils.settings import get_managed

from _typeshed import Incomplete
class IastDeployDesc(models.Model):
    desc: Incomplete = models.TextField(blank=True, null=True)
    middleware: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    language: Incomplete = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'iast_deploy'
