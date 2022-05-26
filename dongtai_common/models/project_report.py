#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:luzhongyang
# datetime:2021/10/29 下午5:29
# software: PyCharm
# project: dongtai-models
from django.db import models
from django.utils.translation import gettext_lazy as _

from dongtai_common.models import User
from dongtai_common.models.project import IastProject
from dongtai_common.models.server import IastServer
from dongtai_common.utils.settings import get_managed


class ProjectReport(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    project = models.ForeignKey(IastProject, models.DO_NOTHING, blank=True, null=True)
    vul_id = models.IntegerField(blank=True, null=True, default=0)
    type = models.CharField(max_length=10, blank=True, null=True)
    language = models.CharField(max_length=10, blank=True, null=True)
    status = models.IntegerField(default=0, null=False)
    path = models.CharField(default='', max_length=255, blank=True, null=True)
    file = models.BinaryField(blank=True, null=True)
    create_time = models.IntegerField(default=0, null=False)

    class Meta:
        managed = get_managed()
        db_table = 'iast_project_report'
