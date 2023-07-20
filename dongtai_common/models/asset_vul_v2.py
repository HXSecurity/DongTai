from dongtai_common.models.assetv2 import AssetV2Global, AssetRiskLevel
from django.db import models
from dongtai_common.utils.settings import get_managed


class IastAssetVulV2(models.Model):
    vul_name = models.CharField(max_length=255, blank=True)
    vul_detail = models.TextField()
    # 漏洞类型等级
    level = models.IntegerField(
        choices=AssetRiskLevel.choices,
        blank=True,
        db_column="level_id",
        default=AssetRiskLevel.LOW,
    )
    update_time = models.IntegerField()
    create_time = models.IntegerField()
    references = models.JSONField(default=list)
    change_time = models.IntegerField()
    published_time = models.IntegerField()
    vul_id = models.CharField(max_length=255, unique=True, blank=True)
    vul_type = models.JSONField()
    vul_codes = models.JSONField()
    affected_versions = models.JSONField()
    unaffected_versions = models.JSONField()

    class Meta:
        managed = True
        db_table = "iast_asset_vul_v2"


class IastVulAssetRelationV2(models.Model):
    asset_vul = models.ForeignKey(
        IastAssetVulV2,
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        db_column="vul_id",
        to_field="vul_id",
    )
    asset = models.ForeignKey(
        AssetV2Global,
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        db_column="asset",
        to_field="aql",
    )

    class Meta:
        managed = get_managed()
        db_table = "iast_asset_vul_v2_relation"


# class IastPackageGAInfo(models.Model):
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
