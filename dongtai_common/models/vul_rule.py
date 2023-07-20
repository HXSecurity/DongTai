#!/usr/bin/env python
# -*- coding:utf-8 -*-
# datetime:2021/2/19 下午3:04
from django.db import models
from dongtai_common.utils.settings import get_managed


class IastVulRule(models.Model):
    rule_name = models.CharField(max_length=255, blank=True, null=True)
    rule_level = models.CharField(max_length=10, blank=True, null=True)
    rule_msg = models.CharField(max_length=255, blank=True, null=True)
    rule_value = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_enable = models.IntegerField(blank=True, null=True)
    is_system = models.IntegerField(blank=True, null=True)
    create_by = models.IntegerField(blank=True, null=True)
    create_time = models.IntegerField(blank=True, null=True)
    update_time = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = get_managed()
        db_table = "iast_vul_rule"
