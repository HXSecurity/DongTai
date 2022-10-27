#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/14 下午2:54
# software: PyCharm
# project: dongtai-models
from django.db import models
from dongtai_common.utils.settings import get_managed

from dongtai_common.models.agent import IastAgent


from _typeshed import Incomplete
class IastAgentProperties(models.Model):
    hook_type: Incomplete = models.IntegerField(blank=True, null=True)
    dump_class: Incomplete = models.IntegerField(blank=True, null=True)
    create_time: Incomplete = models.IntegerField(blank=True, null=True)
    update_time: Incomplete = models.IntegerField(blank=True, null=True)
    updated_by: Incomplete = models.IntegerField(blank=True, null=True)
    agent: Incomplete = models.ForeignKey(IastAgent, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'iast_agent_properties'
