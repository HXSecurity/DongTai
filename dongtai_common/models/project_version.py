#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:sjh
# datetime:2021/06/08 下午5:32
# software: PyCharm
# project: dongtai-models
import time
from django.db import models
from dongtai_common.models import User
from dongtai_common.models.project import IastProject
from django.utils.translation import gettext_lazy as _
from dongtai_common.utils.settings import get_managed


class IastProjectVersion(models.Model):
    version_name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    current_version = models.PositiveSmallIntegerField(blank=True, default=0)
    status = models.PositiveSmallIntegerField(blank=True, null=True)
    create_time = models.IntegerField(_('create time'), default=int(time.time()), blank=True)
    update_time = models.IntegerField(_('update time'), default=int(time.time()), blank=True)
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    project = models.ForeignKey(IastProject, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = get_managed()
        db_table = 'iast_project_version'
