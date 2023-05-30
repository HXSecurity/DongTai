#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/8/20 15:10
# software: PyCharm
# project: dongtai-models

import uuid
from django.core.cache import cache
from django_elasticsearch_dsl.search import Search
from dongtai_conf.settings import ASSET_INDEX
from django_elasticsearch_dsl import Document, fields
from django.db.models.fields.related import ForeignKey
from dongtai_web.utils import get_model_field
from django_elasticsearch_dsl.registries import registry
from django_elasticsearch_dsl import Document
from django.db import models
from django.utils.translation import gettext_lazy as _

from dongtai_common.models import User
from dongtai_common.models.agent import IastAgent
from dongtai_common.models.project import IastProject
from dongtai_common.models.project_version import IastProjectVersion
from dongtai_common.models.vul_level import IastVulLevel
from dongtai_common.utils.settings import get_managed
from dongtai_common.models.department import Department
from dongtai_common.models.talent import Talent


class AssetV2(models.Model):
    id = models.BigAutoField(primary_key=True)
    package_name = models.CharField(max_length=255, blank=True, null=True)
    aql = models.ForeignKey('AssetV2Global',
                            to_field='aql',
                            default='',
                            on_delete=models.DO_NOTHING)
    package_path = models.CharField(max_length=255, blank=True, null=True)
    signature_algorithm = models.CharField(max_length=255,
                                           blank=True,
                                           null=True)
    signature_value = models.CharField(max_length=255, blank=True, null=True)
    dt = models.IntegerField(blank=True, null=True)
    is_reconized = models.IntegerField(blank=True, null=True)
    version = models.CharField(max_length=255, blank=True, null=True)
    level = models.ForeignKey(IastVulLevel,
                              models.DO_NOTHING,
                              blank=True,
                              null=True,
                              default=4)
    project = models.ForeignKey(IastProject,
                                on_delete=models.CASCADE,
                                blank=True,
                                null=False,
                                default=-1)
    project_version = models.ForeignKey(IastProjectVersion,
                                        on_delete=models.CASCADE,
                                        blank=True,
                                        null=False,
                                        default=-1)
    language = models.CharField(max_length=32,
                                blank=True,
                                null=False,
                                default='')

    # 部门id
    department = models.ForeignKey(Department,
                                   models.DO_NOTHING,
                                   blank=True,
                                   null=True,
                                   default=-1)

    class Meta:
        managed = get_managed()
        db_table = 'iast_asset_v2'


class AssetV2Global(models.Model):
    id = models.BigAutoField(primary_key=True)
    aql = models.CharField(max_length=255, blank=True, null=True)
    package_name = models.CharField(max_length=255, blank=True, null=True)
    signature_algorithm = models.CharField(max_length=255,
                                           blank=True,
                                           null=True)
    signature_value = models.CharField(max_length=255, blank=True, null=True)
    version = models.CharField(max_length=255, blank=True, null=True)
    level = models.ForeignKey(IastVulLevel,
                              models.DO_NOTHING,
                              blank=True,
                              null=True,
                              default=4)
    vul_count = models.IntegerField(blank=True, null=True)
    vul_critical_count = models.IntegerField(default=0, blank=True, null=False)
    vul_high_count = models.IntegerField(default=0, blank=True, null=False)
    vul_medium_count = models.IntegerField(default=0, blank=True, null=False)
    vul_low_count = models.IntegerField(default=0, blank=True, null=False)
    vul_info_count = models.IntegerField(default=0, blank=True, null=False)
    language = models.CharField(max_length=32,
                                blank=True,
                                null=False,
                                default='')
    language_id = models.IntegerField(default=1, blank=True, null=False)

    safe_version_list = models.JSONField(blank=True, null=True, default=list)
    license_list = models.JSONField(blank=True, null=True, default=list)

    class Meta:
        managed = get_managed()
        db_table = 'iast_asset_v2_summary'


class IastAssetLicense(models.Model):
    license_id = models.IntegerField(blank=True, null=True)
    license = models.CharField(max_length=64,
                               blank=True,
                               null=False,
                               default='')
    asset = models.ForeignKey(AssetV2Global,
                              on_delete=models.DO_NOTHING,
                              db_constraint=False,
                              db_column='asset_id')
    create_time = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = get_managed()
        db_table = 'iast_asset_v2_license'
