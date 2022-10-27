#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/5/6 下午2:34
# project: dongtai-models
from django.db import models

from dongtai_common.models import User
from dongtai_common.utils.settings import get_managed

from _typeshed import Incomplete
WEB_HOOK: int = 1
GITLAB: int = 2
JIRA: int = 3
ZENDAO: int = 4
FEISHU: int = 5
WEIXIN: int = 6
DING_DING: int = 7



NOTIFY_TYPE_CHOICES: Incomplete = (
    (WEB_HOOK, WEB_HOOK),
    (GITLAB, GITLAB),
    (JIRA, JIRA),
    (ZENDAO, ZENDAO),
    (FEISHU, FEISHU),
    (WEIXIN, WEIXIN),
    (DING_DING, DING_DING),
)


class IastNotifyConfig(models.Model):
    WEB_HOOK: Incomplete = WEB_HOOK
    DING_DING: Incomplete = DING_DING
    FEISHU: Incomplete = FEISHU
    WEIXIN: Incomplete = WEIXIN
    NOTIFY_TYPE_CHOICES: Incomplete = NOTIFY_TYPE_CHOICES

    notify_type: Incomplete = models.SmallIntegerField(blank=True, null=True, choices=NOTIFY_TYPE_CHOICES)
    notify_meta_data: Incomplete = models.TextField(blank=True, null=True)  # This field type is a guess.
    user: Incomplete = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, blank=True, null=True)
    test_result: Incomplete = models.SmallIntegerField(blank=True, null=True,default=0)
    create_time: Incomplete = models.IntegerField(blank=True, null=True)

    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'iast_notify_config'
