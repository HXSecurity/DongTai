# !usr/bin/env python
# @author:zhaoyanwei
# @file: asset_aggr.py
# @time: 2022/5/15  上午12:05

from django.db import models
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from dongtai_common.models.vul_level import IastVulLevel
from dongtai_common.utils.settings import get_managed
from dongtai_conf.settings import ASSET_AGGR_INDEX


class AssetAggr(models.Model):
    package_name = models.CharField(max_length=255, blank=True)
    signature_value = models.CharField(max_length=255, blank=True)
    version = models.CharField(max_length=255, blank=True)
    safe_version = models.CharField(max_length=255, blank=True)
    last_version = models.CharField(max_length=255, blank=True)
    level = models.ForeignKey(IastVulLevel, models.DO_NOTHING)
    vul_count = models.IntegerField()
    vul_critical_count = models.IntegerField(default=0)
    vul_high_count = models.IntegerField(default=0)
    vul_medium_count = models.IntegerField(default=0)
    vul_low_count = models.IntegerField(default=0)
    vul_info_count = models.IntegerField(default=0)
    project_count = models.IntegerField(blank=True)
    language = models.CharField(max_length=32, blank=True)
    license = models.CharField(max_length=64, blank=True)
    is_del = models.SmallIntegerField(default=0)

    class Meta:
        managed = get_managed()
        db_table = "iast_asset_aggr"


@registry.register_document
class AssetAggrDocument(Document):
    level_id = fields.IntegerField(attr="level_id")

    class Index:
        name = ASSET_AGGR_INDEX

    class Django:
        model = AssetAggr

        fields = [
            "id",
            "package_name",
            "signature_value",
            "version",
            "safe_version",
            "last_version",
            "vul_count",
            "vul_critical_count",
            "vul_high_count",
            "vul_medium_count",
            "vul_low_count",
            "vul_info_count",
            "project_count",
            "language",
            "license",
            "is_del",
        ]
