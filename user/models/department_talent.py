#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/13 下午5:50
# software: PyCharm
# project: lingzhi-agent-server
from django.db import models

from user.models.department import AuthDepartment
from user.models.talent import AuthTalent


class AuthDepartmentTalent(models.Model):
    talent = models.ForeignKey(AuthTalent, on_delete=models.DO_NOTHING, blank=True, null=True)
    department = models.ForeignKey(AuthDepartment, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_department_talent'
