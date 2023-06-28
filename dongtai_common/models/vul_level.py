#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/12/4 上午11:54
# software: PyCharm
# project: dongtai-models
from django.db import models
from dongtai_common.utils.settings import get_managed


class IastVulLevel(models.Model):
    name = models.CharField(max_length=255)
    name_value = models.CharField(max_length=255)
    name_type = models.CharField(max_length=255)

    class Meta:
        managed = get_managed()
        db_table = 'iast_vul_level'
