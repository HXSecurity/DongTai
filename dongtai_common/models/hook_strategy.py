#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/13 下午7:14
# software: PyCharm
# project: dongtai-models
from django.db import models
from django.utils.translation import gettext_lazy as _

from dongtai_common.models.hook_type import HookType
from dongtai_common.utils.settings import get_managed
from dongtai_common.models.program_language import IastProgramLanguage
from time import time


# class PermissionsMixin(models.Model):
#    type = models.ManyToManyField(
#        HookType,
#        verbose_name=_('type'),
#        blank=True,
#        help_text=_(
#            'The department this user belongs to. A user will get all permissions '
#            'granted to each of their department.'
#        ),
#        related_name="strategies",
#        related_query_name="strategy",
#    )
#
#    class Meta:
#        abstract = True


class HookStrategy(models.Model):
    value = models.CharField(max_length=255, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    target = models.CharField(max_length=255, blank=True, null=True)
    inherit = models.CharField(max_length=255, blank=True, null=True)
    track = models.CharField(max_length=5, blank=True, null=True)
    create_time = models.IntegerField(blank=True, null=True, default=time)
    update_time = models.IntegerField(blank=True, null=True, default=time)
    created_by = models.IntegerField(
        blank=True,
        null=True,
    )
    enable = models.IntegerField(blank=True, null=False, default=1)
    language = models.ForeignKey(IastProgramLanguage,
                                 blank=True,
                                 default='',
                                 on_delete=models.DO_NOTHING,
                                 db_constraint=False)
    type = models.IntegerField(blank=True, null=True)

    hooktype = models.ForeignKey(
        HookType,
        verbose_name=_('type'),
        blank=True,
        null=True,
        help_text=_(
            'The department this user belongs to. A user will get all permissions '
            'granted to each of their department.'),
        related_name="strategies",
        related_query_name="strategy",
        on_delete=models.DO_NOTHING,
    )
    strategy = models.ForeignKey(
        'dongtai_common.IastStrategyModel',
        blank=True,
        default=-1,
        on_delete=models.DO_NOTHING,
        db_column='strategy_id',
        db_constraint=False,
        related_name="strategies",
        related_query_name="strategy",
    )
    system_type = models.IntegerField(blank=True, null=True, default=0)
    ignore_blacklist = models.BooleanField(blank=True,
                                           null=False,
                                           default=False)
    ignore_internal = models.BooleanField(blank=True,
                                          null=False,
                                          default=False)

    class Meta:
        managed = get_managed()
        db_table = 'iast_hook_strategy'
