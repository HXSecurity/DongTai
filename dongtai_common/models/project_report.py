#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:luzhongyang
# datetime:2021/10/29 下午5:29
# software: PyCharm
# project: dongtai-models
from django.db import models

from dongtai_common.models import User
from dongtai_common.models.project import IastProject
from dongtai_common.utils.settings import get_managed

ORDER_TYPE_REPORT = {
    "1": "create_time",
    "2": "status"
}


class ProjectReport(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    project = models.ForeignKey(IastProject, models.DO_NOTHING)
    type = models.CharField(max_length=10, blank=True)
    language = models.CharField(max_length=10, blank=True)
    status = models.IntegerField(default=0)
    path = models.CharField(max_length=255, blank=True)
    file = models.BinaryField(blank=True, null=True)
    create_time = models.IntegerField(default=0)
    is_del = models.SmallIntegerField(default=0)
    level_png = models.CharField(max_length=255, blank=True, null=True)
    trend_png = models.CharField(max_length=255, blank=True, null=True)
    version_str = models.CharField(max_length=255, blank=True, null=True)
    vul_type_str = models.CharField(max_length=255, blank=True, null=True)
    sca_type_str = models.TextField(blank=True, null=True)
    vul_id = models.IntegerField(default=0)
    report_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = get_managed()
        db_table = 'iast_project_report'
