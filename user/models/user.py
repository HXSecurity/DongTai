#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/12 下午7:11
# software: PyCharm
# project: lingzhi-agent-server
from django.contrib.auth.models import AbstractUser
from django.db import models

from user.models.department import Department


class User(AbstractUser):
    phone = models.CharField(max_length=100)
    upgrade_url = models.CharField(max_length=255, null=True)
    department = models.ForeignKey(Department, models.DO_NOTHING, blank=True, null=True)

    class Meta(AbstractUser.Meta):
        db_table = 'auth_user'
