from dongtai_common.models.asset import Asset
from django.db import models
from dongtai_common.utils.settings import get_managed
from dongtai_common.models.vulnerablity import IastVulnerabilityStatus
from dongtai_common.models.vul_level import IastVulLevel


class IastAssetVul(models.Model):
    vul_name = models.CharField(max_length=255, blank=True, null=True)
    vul_detail = models.TextField(blank=True, null=True)
    # 漏洞类型等级
    level = models.ForeignKey(IastVulLevel,
                              models.DO_NOTHING,
                              blank=True,
                              null=True)
    license = models.CharField(max_length=50, blank=True, null=True)
    # 开源许可证 风险等级  # 1 高 2中 3低 0无风险
    license_level = models.SmallIntegerField(blank=True, null=True)
    aql = models.CharField(max_length=100, blank=True, null=True)
    package_name = models.CharField(max_length=100, blank=True, null=True)
    package_hash = models.CharField(max_length=100, blank=True, null=True)
    package_version = models.CharField(max_length=50, blank=True, null=True)
    package_safe_version = models.CharField(max_length=50, blank=True, null=True)
    package_latest_version = models.CharField(max_length=50, blank=True, null=True)
    package_language = models.CharField(max_length=10, blank=True, null=True)
    vul_cve_nums = models.JSONField(blank=True, null=True)
    vul_serial = models.CharField(max_length=100, blank=True, null=True)  # 漏洞编号  CWE|CVE等数据
    have_article = models.SmallIntegerField(blank=True, null=True)
    have_poc = models.SmallIntegerField(blank=True, null=True)
    cve_code = models.CharField(max_length=64, blank=True, null=True)
    cve_id = models.IntegerField(blank=True, null=True)
    update_time = models.IntegerField(blank=True, null=True)
    update_time_desc = models.IntegerField(blank=True, null=True)
    create_time = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'iast_asset_vul'


class IastVulAssetRelation(models.Model):
    asset_vul = models.ForeignKey(IastAssetVul,
                                  on_delete=models.CASCADE,
                                  db_constraint=False,
                                  db_column='asset_vul_id')
    asset = models.ForeignKey(Asset,
                              on_delete=models.CASCADE,
                              db_constraint=False,
                              db_column='asset_id')
    status = models.ForeignKey(IastVulnerabilityStatus,
                               on_delete=models.DO_NOTHING,
                               db_constraint=False,
                               db_column='status_id')
    is_del = models.SmallIntegerField(blank=True, null=False, default=0)
    create_time = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = get_managed()
        db_table = 'iast_asset_vul_relation'
        unique_together = ['asset_vul_id', 'asset_id']


class IastAssetVulType(models.Model):
    cwe_id = models.CharField(max_length=20, blank=True, null=True, default='')
    name = models.CharField(max_length=100, blank=True, null=True, default='')

    class Meta:
        managed = get_managed()
        db_table = 'iast_asset_vul_type'


class IastAssetVulTypeRelation(models.Model):
    asset_vul = models.ForeignKey(IastAssetVul,
                                  on_delete=models.CASCADE,
                                  db_constraint=False,
                                  db_column='asset_vul_id')
    asset_vul_type = models.ForeignKey(IastAssetVulType,
                                       on_delete=models.CASCADE,
                                       db_constraint=False,
                                       db_column='asset_vul_type_id')

    class Meta:
        managed = get_managed()
        db_table = 'iast_asset_vul_type_relation'

    # "iast_asset_vul_type_relation      iast_asset_vul_relation  iast_asset_vul iast_asset "