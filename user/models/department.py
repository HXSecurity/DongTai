#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/13 下午5:50
# software: PyCharm
# project: lingzhi-agent-server
from django.db import models


class AuthDepartment(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.IntegerField(blank=True, null=True)
    update_time = models.IntegerField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_department'
