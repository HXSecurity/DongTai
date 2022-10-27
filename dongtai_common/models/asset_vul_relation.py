#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/8/20 15:10
# software: PyCharm
# project: dongtai-models

from django.db import models
from dongtai_common.models.project import IastProject
from dongtai_common.models.project_version import IastProjectVersion
from dongtai_common.models.agent import IastAgent
from dongtai_common.models.user import User
from dongtai_common.models.talent import Talent
from dongtai_common.models.department import Department
from dongtai_common.utils.settings import get_managed
from dongtai_web.dongtai_sca.models import VulPackage
from dongtai_common.models.aql_info import AqlInfo


from _typeshed import Incomplete
class AssetVulRelation(models.Model):
    id: Incomplete = models.BigAutoField(primary_key=True)
    hash: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    create_time: Incomplete = models.IntegerField(blank=True, null=True)
    is_del: Incomplete = models.SmallIntegerField(blank=True, null=True)
    talent: Incomplete = models.ForeignKey(
        to=Talent,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True
    )

    department: Incomplete = models.ForeignKey(
        to=Department,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True
    )


    user: Incomplete = models.ForeignKey(
        to=User,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True
    )

    project_version: Incomplete = models.ForeignKey(
        to=IastProjectVersion,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True
    )

    project: Incomplete = models.ForeignKey(
        to=IastProject,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True
    )

    agent: Incomplete = models.ForeignKey(
        to=IastAgent,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True
    )
    vul_package: Incomplete = models.ForeignKey(
        to=VulPackage,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True
    )
    aql_info: Incomplete = models.ForeignKey(
        to=AqlInfo,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True
    )

    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'iast_asset_vul_relation'
