#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/8/20 15:10
# software: PyCharm
# project: dongtai-models

import time
from django.db import models
from django.utils.translation import gettext_lazy as _

from dongtai_common.models.project import IastProject
from dongtai_common.models.project_version import IastProjectVersion
from dongtai_common.utils.settings import get_managed
from dongtai_common.models.department import Department
from django.db.models import IntegerChoices


class AssetRiskLevel(IntegerChoices):
    CRITICAL = 4, _("严重")
    HIGH = 3, _("高危")
    MODERATE = 2, _("中危")
    LOW = 1, _("低危")
    NO_RISK = 0, _("无风险")


class AssetV2(models.Model):
    id = models.BigAutoField(primary_key=True)
    package_name = models.CharField(max_length=255, unique=True, blank=True)
    package_path = models.CharField(max_length=255, blank=True)
    signature_algorithm = models.CharField(max_length=255, blank=True)
    signature_value = models.CharField(max_length=255, blank=True)
    dt = models.IntegerField(blank=True, default=lambda: int(time.time()))
    version = models.CharField(max_length=255, blank=True)
    project = models.ForeignKey(IastProject,
                                on_delete=models.CASCADE,
                                blank=True,
                                default=-1)
    project_version = models.ForeignKey(IastProjectVersion,
                                        on_delete=models.CASCADE,
                                        blank=True,
                                        default=-1)
    # 部门id
    department = models.ForeignKey(Department,
                                   models.DO_NOTHING,
                                   blank=True,
                                   default=-1)
    language_id = models.IntegerField(default=1, blank=True)
    #is_reconized = models.IntegerField(blank=True, null=True)
    aql = models.ForeignKey('AssetV2Global',
                            to_field='aql',
                            blank=True,
                            db_column="aql",
                            on_delete=models.DO_NOTHING)

    class Meta:
        managed = get_managed()
        db_table = 'iast_asset_v2'


class AssetV2Global(models.Model):
    id = models.BigAutoField(primary_key=True)
    package_name = models.CharField(max_length=255, blank=True)
    package_fullname = models.ForeignKey(
        'IastPackageGAInfo',
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        db_column="package_fullname",
        to_field="package_fullname",
    )
    signature_algorithm = models.CharField(max_length=255, blank=True)
    signature_value = models.CharField(max_length=255, blank=True)
    version = models.CharField(max_length=255, blank=True)
    level = models.IntegerField(
        choices=AssetRiskLevel.choices,
        blank=True,
        default=AssetRiskLevel.NO_RISK,
        db_column="level_id",
    )
    vul_count = models.IntegerField(default=0, blank=True)
    vul_critical_count = models.IntegerField(default=0, blank=True)
    vul_high_count = models.IntegerField(default=0, blank=True)
    vul_medium_count = models.IntegerField(default=0, blank=True)
    vul_low_count = models.IntegerField(default=0, blank=True)
    vul_info_count = models.IntegerField(default=0, blank=True)
    license_list = models.JSONField(blank=True, default=list)
    language_id = models.IntegerField(default=1, blank=True)
    aql = models.CharField(max_length=255, blank=True, unique=True)

    class Meta:
        managed = get_managed()
        db_table = 'iast_asset_v2_global'

    def get_vul_count_groupby_level(self):
        return [
            {
                "label": "严重",
                "count": self.vul_critical_count,
            },
            {
                "label": "高危",
                "count": self.vul_high_count,
            },
            {
                "label": "中危",
                "count": self.vul_medium_count,
            },
            {
                "label": "低危",
                "count": self.vul_low_count,
            },
        ]


class IastAssetLicense(models.Model):
    """
    only for the filter
    """
    license_id = models.IntegerField()
    asset = models.ForeignKey(AssetV2Global,
                              on_delete=models.DO_NOTHING,
                              db_constraint=False,
                              db_column='asset',
                              to_field='aql')

    class Meta:
        managed = get_managed()
        db_table = 'iast_asset_v2_license'


class IastPackageGAInfo(models.Model):
    package_fullname = models.CharField(max_length=255, unique=True, blank=True)
    affected_versions = models.JSONField(blank=True, default=list)
    unaffected_versions = models.JSONField(blank=True, default=list)

    class Meta:
        managed = get_managed()
        db_table = 'iast_asset_v2_ga_info'
