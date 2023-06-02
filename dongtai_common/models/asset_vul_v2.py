import uuid
from dongtai_common.models.agent import IastAgent
from django.core.cache import cache
from django_elasticsearch_dsl.search import Search
from dongtai_conf.settings import ASSET_VUL_INDEX
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from dongtai_common.models.assetv2 import AssetV2Global
from django.db import models
from dongtai_common.utils.settings import get_managed
from dongtai_common.models.vulnerablity import IastVulnerabilityStatus
from dongtai_common.models.vul_level import IastVulLevel


class IastAssetVulV2(models.Model):
    vul_name = models.CharField(max_length=255, blank=True, null=True)
    vul_detail = models.TextField(blank=True, null=True)
    # 漏洞类型等级
    level = models.ForeignKey(IastVulLevel,
                              models.DO_NOTHING,
                              blank=True,
                              null=True)
    update_time = models.IntegerField(blank=True, null=True)
    create_time = models.IntegerField(blank=True, null=True)
    references = models.JSONField(blank=True, null=True, default=list)
    change_time = models.IntegerField(blank=True, null=True)
    published_time = models.IntegerField(blank=True, null=True)
    vul_id = models.CharField(max_length=255,
                              blank=True,
                              null=True,
                              unique=True)
    vul_type = models.JSONField(blank=True, null=True)
    vul_codes = models.JSONField(blank=True, null=True)
    affected_versions = models.JSONField(blank=True, null=True)
    unaffected_versions = models.JSONField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'iast_asset_vul_v2'


class IastVulAssetRelationV2(models.Model):
    asset_vul = models.ForeignKey(IastAssetVulV2,
                                  on_delete=models.DO_NOTHING,
                                  db_constraint=False,
                                  db_column='vul_id',
                                  to_field="vul_id")
    asset = models.ForeignKey(AssetV2Global,
                              on_delete=models.DO_NOTHING,
                              db_constraint=False,
                              db_column='asset',
                              to_field="aql")

    class Meta:
        managed = get_managed()
        db_table = 'iast_asset_vul_v2_relation'


#class IastPackageGAInfo(models.Model):
#    package_name = models.ForeignKey(AssetV2Global,
#                                     on_delete=models.DO_NOTHING,
#                                     db_constraint=False,
#                                     db_column='package_name')
#    affected_versions = models.JSONField(blank=True, null=True, default=list)
#    unaffected_versions = models.JSONField(blank=True, null=True, default=list)
#
#    class Meta:
#        managed = get_managed()
#        db_table = 'iast_asset_v2_ga_info'
