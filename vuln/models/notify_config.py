#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/5/6 下午2:34
# project: dongtai-engine
from django.db import models

from account.models import User

WEB_HOOK = 1
DING_DING = 2
JIRA = 3
EMAIL = 4

NOTIFY_TYPE_CHOICES = (
    (WEB_HOOK, WEB_HOOK),
    (DING_DING, DING_DING),
    (JIRA, JIRA),
    (EMAIL, EMAIL),
)


class IastNotifyConfig(models.Model):
    WEB_HOOK = WEB_HOOK
    DING_DING = DING_DING
    JIRA = JIRA
    EMAIL = EMAIL

    NOTIFY_TYPE_CHOICES = NOTIFY_TYPE_CHOICES

    notify_type = models.IntegerField(blank=True, null=True, choices=NOTIFY_TYPE_CHOICES)
    notify_metadata = models.TextField(blank=True, null=True)  # This field type is a guess.
    user = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'iast_notify_config'
