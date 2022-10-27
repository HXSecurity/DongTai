#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/2/19 下午3:04
# software: PyCharm
# project: dongtai-models
from django.db import models
from dongtai_common.utils.settings import get_managed


from _typeshed import Incomplete
class IastVulRule(models.Model):
    rule_name: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    rule_level: Incomplete = models.CharField(max_length=10, blank=True, null=True)
    rule_msg: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    rule_value: Incomplete = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_enable: Incomplete = models.IntegerField(blank=True, null=True)
    is_system: Incomplete = models.IntegerField(blank=True, null=True)
    create_by: Incomplete = models.IntegerField(blank=True, null=True)
    create_time: Incomplete = models.IntegerField(blank=True, null=True)
    update_time: Incomplete = models.IntegerField(blank=True, null=True)

    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'iast_vul_rule'
