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


#class PermissionsMixin(models.Model):
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


from _typeshed import Incomplete
class HookStrategy(models.Model):
    value: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    source: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    target: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    inherit: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    track: Incomplete = models.CharField(max_length=5, blank=True, null=True)
    create_time: Incomplete = models.IntegerField(blank=True, null=True, default=time)
    update_time: Incomplete = models.IntegerField(blank=True, null=True, default=time)
    created_by: Incomplete = models.IntegerField(
        blank=True,
        null=True,
    )
    enable: Incomplete = models.IntegerField(blank=True, null=False, default=1)
    language: Incomplete = models.ForeignKey(IastProgramLanguage,
                                 blank=True,
                                 default='',
                                 on_delete=models.DO_NOTHING,
                                 db_constraint=False)
    type: Incomplete = models.IntegerField(blank=True, null=True)

    hooktype: Incomplete = models.ForeignKey(
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
    strategy: Incomplete = models.ForeignKey(
        'dongtai_common.IastStrategyModel',
        blank=True,
        default=-1,
        on_delete=models.DO_NOTHING,
        db_column='strategy_id',
        db_constraint=False,
        related_name="strategies",
        related_query_name="strategy",
    )
    system_type: Incomplete = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'iast_hook_strategy'
