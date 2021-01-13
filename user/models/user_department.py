#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/13 下午5:50
# software: PyCharm
# project: lingzhi-agent-server
from django.db import models

from user.models import User
from user.models.department import AuthDepartment


class AuthUserDepartment(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    department = models.ForeignKey(AuthDepartment, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_user_department'
