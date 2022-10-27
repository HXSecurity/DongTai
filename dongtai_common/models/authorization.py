#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/5/25 14:48
# software: PyCharm
# project: dongtai-models
from django.db import models
from dongtai_common.utils.settings import get_managed


from _typeshed import Incomplete
class IastAuthorization(models.Model):
    user_id: Incomplete = models.IntegerField(blank=True, null=True)
    token: Incomplete = models.CharField(max_length=50, blank=True, null=True)
    view_name: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    state: Incomplete = models.CharField(max_length=20, blank=True, null=True)
    dt: Incomplete = models.IntegerField(blank=True, null=True)

    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'iast_authorization'
