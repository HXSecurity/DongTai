#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/8/20 15:10
# software: PyCharm
# project: dongtai-models

from django.db import models
from django.utils.translation import gettext_lazy as _

from dongtai.models.agent import IastAgent
from dongtai.models.vul_level import IastVulLevel
from dongtai.utils.settings import get_managed


class Asset(models.Model):
    package_name = models.CharField(max_length=255, blank=True, null=True)
    package_path = models.CharField(max_length=255, blank=True, null=True)
    signature_algorithm = models.CharField(max_length=255, blank=True, null=True)
    signature_value = models.CharField(max_length=255, blank=True, null=True)
    dt = models.IntegerField(blank=True, null=True)
    version = models.CharField(max_length=255, blank=True, null=True)
    level = models.ForeignKey(IastVulLevel, models.DO_NOTHING, blank=True, null=True)
    vul_count = models.IntegerField(blank=True, null=True)
    agent = models.ForeignKey(
        to=IastAgent,
        on_delete=models.DO_NOTHING,
        related_name='assets',
        related_query_name='asset',
        verbose_name=_('agent'),
        blank=True,
        null=True
    )

    class Meta:
        managed = get_managed()
        db_table = 'iast_asset'
