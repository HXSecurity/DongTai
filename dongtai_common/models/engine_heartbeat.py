#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/5/6 下午5:56
# project: dongtai-models
from django.db import models
from dongtai_common.utils.settings import get_managed


from _typeshed import Incomplete
class IastEngineHeartbeat(models.Model):
    client_ip: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    status: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    msg: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    agentcount: Incomplete = models.IntegerField(db_column='agentCount', blank=True, null=True)  # Field name made lowercase.
    reqcount: Incomplete = models.BigIntegerField(db_column='reqCount', blank=True, null=True)  # Field name made lowercase.
    agentenablecount: Incomplete = models.IntegerField(db_column='agentEnableCount', blank=True,
                                           null=True)  # Field name made lowercase.
    projectcount: Incomplete = models.IntegerField(db_column='projectCount', blank=True, null=True)  # Field name made lowercase.
    usercount: Incomplete = models.IntegerField(db_column='userCount', blank=True, null=True)  # Field name made lowercase.
    vulcount: Incomplete = models.IntegerField(db_column='vulCount', blank=True, null=True)  # Field name made lowercase.
    methodpoolcount: Incomplete = models.IntegerField(db_column='methodPoolCount', blank=True,
                                          null=True)  # Field name made lowercase.
    timestamp: Incomplete = models.IntegerField(blank=True, null=True)

    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'iast_engine_heartbeat'
