#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/5/10 下午2:24
# project: dongtai-models
from django.contrib.auth.models import Group
from django.db import models

from dongtai_common.models import User
from dongtai_common.utils.settings import get_managed


from _typeshed import Incomplete
class AuthGroupRoutes(models.Model):
    is_active: Incomplete = models.IntegerField(blank=True, null=True)
    routes: Incomplete = models.JSONField(blank=True, null=True)
    group: Incomplete = models.ForeignKey(Group, models.DO_NOTHING, blank=True, null=True)
    created_by: Incomplete = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    create_time: Incomplete = models.IntegerField(blank=True, null=True)
    update_time: Incomplete = models.IntegerField(blank=True, null=True)

    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'auth_group_routes'
