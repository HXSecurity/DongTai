from django.db import models

from dongtai_common.models.assetv2 import AssetRiskLevel, AssetV2Global
from dongtai_common.utils.settings import get_managed


class IastAssetVulV2(models.Model):
    vul_name = models.CharField(max_length=255, blank=True, help_text="漏洞名")
    vul_name_zh = models.CharField(max_length=255, blank=True, help_text="漏洞名(中文)")
    vul_detail = models.TextField(help_text="漏洞详情")
    vul_detail_zh = models.TextField(blank=True, help_text="漏洞详情(中文)")
    # 漏洞类型等级
    level = models.IntegerField(
        choices=AssetRiskLevel.choices, blank=True, db_column="level_id", default=AssetRiskLevel.LOW, help_text="漏洞等级"
    )
    update_time = models.IntegerField(help_text="更新时间")
    create_time = models.IntegerField(help_text="创建时间")
    references = models.JSONField(default=list, help_text="引用文章")
    change_time = models.IntegerField(help_text="修改时间")
    published_time = models.IntegerField(help_text="发布时间")
    vul_id = models.CharField(max_length=255, unique=True, blank=True, help_text="漏洞id")
    vul_type = models.JSONField(help_text="漏洞类型")
    vul_codes = models.JSONField(help_text="漏洞编号")
    affected_versions = models.JSONField(help_text="影响版本")
    unaffected_versions = models.JSONField(help_text="不影响版本")

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
#                                     db_column='package_name')
#
#    class Meta:
