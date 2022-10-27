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

from _typeshed import Incomplete
ORDER_TYPE_REPORT: Incomplete = {
    "1":"create_time",
    "2":"status"
}

class ProjectReport(models.Model):
    user: Incomplete = models.ForeignKey(User, models.DO_NOTHING)
    project: Incomplete = models.ForeignKey(IastProject, models.DO_NOTHING, blank=True, null=True)
    type: Incomplete = models.CharField(max_length=10, blank=True, null=True)
    language: Incomplete = models.CharField(max_length=10, blank=True, null=True)
    status: Incomplete = models.IntegerField(default=0, null=False)
    path: Incomplete = models.CharField(default='', max_length=255, blank=True, null=True)
    file: Incomplete = models.BinaryField(blank=True, null=True)
    create_time: Incomplete = models.IntegerField(default=0, null=False)
    is_del: Incomplete = models.SmallIntegerField(default=0, null=False)
    level_png: Incomplete = models.CharField(default='', max_length=255, blank=True, null=True)
    trend_png: Incomplete = models.CharField(default='', max_length=255, blank=True, null=True)
    version_str: Incomplete = models.CharField(default='', max_length=255, blank=True, null=True)
    vul_type_str: Incomplete = models.CharField(default='', max_length=255, blank=True, null=True)
    sca_type_str: Incomplete = models.TextField(default='',  blank=True, null=True)
    vul_id: Incomplete = models.IntegerField(blank=True, null=True, default=0)
    report_name: Incomplete = models.CharField(default='', max_length=255, blank=True, null=True)

    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'iast_project_report'
