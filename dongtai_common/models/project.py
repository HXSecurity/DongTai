#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/30 下午5:32
# software: PyCharm
# project: dongtai-models
from django.db import models

from dongtai_common.models import User
from dongtai_common.models.strategy_user import IastStrategyUser
from dongtai_common.utils.settings import get_managed
import time


from _typeshed import Incomplete
class VulValidation(models.IntegerChoices):
    FOLLOW_GLOBAL: int = 0
    ENABLE: int = 1
    DISABLE: int = 2
    __empty__: int = 0


class IastProject(models.Model):
    scan: Incomplete
    name: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    mode: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    vul_count: Incomplete = models.PositiveIntegerField(blank=True, null=True)
    agent_count: Incomplete = models.IntegerField(blank=True, null=True)
    latest_time: Incomplete = models.IntegerField(blank=True, null=True)
    user: Incomplete = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    # openapi服务不必使用该字段
    scan = models.ForeignKey(IastStrategyUser,
                             models.DO_NOTHING,
                             blank=True,
                             null=True)


    vul_validation: Incomplete = models.IntegerField(default=0,
                                         blank=True,
                                         null=False,
                                         choices=VulValidation.choices)
    base_url: Incomplete = models.CharField(max_length=255, blank=True, default='')
    test_req_header_key: Incomplete = models.CharField(max_length=511,
                                           blank=True,
                                           default='')
    test_req_header_value: Incomplete = models.CharField(max_length=511,
                                             blank=True,
                                             default='')

    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'iast_project'

    def update_latest(self) -> None:
        self.latest_time = int(time.time())
        self.save(update_fields=['latest_time'])
