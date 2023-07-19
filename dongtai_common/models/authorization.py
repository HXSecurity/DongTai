#!/usr/bin/env python
# datetime:2020/5/25 14:48
from django.db import models

from dongtai_common.utils.settings import get_managed


class IastAuthorization(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    token = models.CharField(max_length=50, blank=True, null=True)
    view_name = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=20, blank=True, null=True)
    dt = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = get_managed()
        db_table = "iast_authorization"
