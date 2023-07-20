#!/usr/bin/env python
# -*- coding:utf-8 -*-
# datetime: 2021/5/6 下午2:34
from django.db import models

from dongtai_common.models import User
from dongtai_common.utils.settings import get_managed

WEB_HOOK = 1
GITLAB = 2
JIRA = 3
ZENDAO = 4
FEISHU = 5
WEIXIN = 6
DING_DING = 7


NOTIFY_TYPE_CHOICES = (
    (WEB_HOOK, WEB_HOOK),
    (GITLAB, GITLAB),
    (JIRA, JIRA),
    (ZENDAO, ZENDAO),
    (FEISHU, FEISHU),
    (WEIXIN, WEIXIN),
    (DING_DING, DING_DING),
)


class IastNotifyConfig(models.Model):
    WEB_HOOK = WEB_HOOK
    DING_DING = DING_DING
    FEISHU = FEISHU
    WEIXIN = WEIXIN
    NOTIFY_TYPE_CHOICES = NOTIFY_TYPE_CHOICES

    notify_type = models.SmallIntegerField(choices=NOTIFY_TYPE_CHOICES)
    notify_meta_data = models.TextField()  # This field type is a guess.
    user = models.ForeignKey(
        to=User,
        on_delete=models.DO_NOTHING,
    )
    test_result = models.SmallIntegerField(default=0)
    create_time = models.IntegerField()

    class Meta:
        managed = get_managed()
        db_table = "iast_notify_config"
