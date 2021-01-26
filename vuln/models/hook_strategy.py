#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/13 下午7:14
# software: PyCharm
# project: lingzhi-agent-server
from django.db import models


# class PermissionsMixin(models.Model):
#     hook_strategy_type = models.ManyToManyField(
#         TypeRelation,
#         verbose_name=_('department'),
#         blank=True,
#         help_text=_(
#             'The department this user belongs to. A user will get all permissions '
#             'granted to each of their department.'
#         ),
#         related_name="hook_strategies",
#         related_query_name="HookStrategy",
#     )
#
#     class Meta:
#         abstract = True


class HookStrategy(models.Model):
    value = models.CharField(max_length=255, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    target = models.CharField(max_length=255, blank=True, null=True)
    inherit = models.CharField(max_length=255, blank=True, null=True)
    track = models.CharField(max_length=5, blank=True, null=True)
    create_time = models.IntegerField(blank=True, null=True)
    update_time = models.IntegerField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'iast_hook_strategy'
