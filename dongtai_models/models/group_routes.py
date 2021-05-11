#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/5/10 下午2:24
# project: dongtai-models
from django.contrib.auth.models import Group
from django.db import models

from dongtai_models.models import User


class AuthGroupRoutes(models.Model):
    is_active = models.IntegerField(blank=True, null=True)
    routes = models.JSONField(blank=True, null=True)
    group = models.ForeignKey(Group, models.DO_NOTHING, blank=True, null=True)
    created_by = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    create_time = models.IntegerField(blank=True, null=True)
    update_time = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_group_routes'
