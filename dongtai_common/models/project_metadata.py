#!/usr/bin/env python
# datetime:2021/06/08 下午5:32

from django.db import models

from dongtai_common.models.project import IastProject
from dongtai_common.models.project_version import IastProjectVersion
from dongtai_common.utils.settings import get_managed


class IastProjectMetaData(models.Model):
    project = models.OneToOneField(IastProject, models.CASCADE, db_constraint=False, unique=True)
    project_version = models.ForeignKey(
        IastProjectVersion, on_delete=models.DO_NOTHING, blank=True, default=-1, db_constraint=False
    )
    api_count = models.IntegerField(help_text="API数量统计", default=0)
    vul_api_count = models.IntegerField(help_text="漏洞API数量统计", default=0)
    create_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        managed = get_managed()
        db_table = "iast_project_meta_data"
