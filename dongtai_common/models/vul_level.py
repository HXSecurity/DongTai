#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/12/4 上午11:54
# software: PyCharm
# project: dongtai-models
from django.db import models
from dongtai_common.utils.settings import get_managed


from _typeshed import Incomplete
class IastVulLevel(models.Model):
    name: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    name_value: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    name_type: Incomplete = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'iast_vul_level'
