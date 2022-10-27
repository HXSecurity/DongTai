# !usr/bin/env python
# coding:utf-8
# @author:zhaoyanwei
# @file: asset_aggr.py
# @time: 2022/5/15  上午12:05

from django.db import models
from dongtai_common.models.vul_level import IastVulLevel
from dongtai_common.utils.settings import get_managed


from _typeshed import Incomplete
class AssetAggr(models.Model):
    package_name: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    signature_value: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    version: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    safe_version: Incomplete = models.CharField(max_length=255, blank=True, null=False, default='')
    last_version: Incomplete = models.CharField(max_length=255, blank=True, null=False, default='')
    level: Incomplete = models.ForeignKey(IastVulLevel, models.DO_NOTHING, blank=True, null=True)
    vul_count: Incomplete = models.IntegerField(blank=True, null=True)
    vul_critical_count: Incomplete = models.IntegerField(default=0, blank=True, null=False)
    vul_high_count: Incomplete = models.IntegerField(default=0, blank=True, null=False)
    vul_medium_count: Incomplete = models.IntegerField(default=0, blank=True, null=False)
    vul_low_count: Incomplete = models.IntegerField(default=0, blank=True, null=False)
    vul_info_count: Incomplete = models.IntegerField(default=0, blank=True, null=False)
    project_count: Incomplete = models.IntegerField(blank=True, null=False, default=0)
    language: Incomplete = models.CharField(max_length=32, blank=True, null=False, default='')
    license: Incomplete = models.CharField(max_length=64, blank=True, null=False, default='')
    is_del: Incomplete = models.SmallIntegerField(blank=True, null=False, default=0)

    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'iast_asset_aggr'


from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from django_elasticsearch_dsl import Document, fields
from dongtai_conf.settings import ASSET_AGGR_INDEX 


@registry.register_document
class AssetAggrDocument(Document):
    level_id: Incomplete = fields.IntegerField(attr="level_id")

    class Index:
        name: Incomplete = ASSET_AGGR_INDEX

    class Django:
        model: Incomplete = AssetAggr

        fields: Incomplete = [
            'id', 'package_name', 'signature_value', 'version', 'safe_version',
            'last_version', 'vul_count', 'vul_critical_count',
            'vul_high_count', 'vul_medium_count', 'vul_low_count',
            'vul_info_count', 'project_count', 'language', 'license', 'is_del',
        ]
