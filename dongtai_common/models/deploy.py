#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/6/3 11:36
# software: PyCharm
# project: dongtai-models

from django.db import models
from dongtai_common.utils.settings import get_managed


class IastDeployDesc(models.Model):
    desc = models.TextField()
    middleware = models.CharField(max_length=255, blank=True)
    language = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = get_managed()
        db_table = 'iast_deploy'
