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
    vul_publish_time = models.DateTimeField(blank=True, null=True)
    vul_update_time = models.DateTimeField(blank=True, null=True)
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
from django_elasticsearch_dsl.registries import registry
from django_elasticsearch_dsl import Document, fields
from dongtai_conf.settings import ASSET_VUL_INDEX
from django_elasticsearch_dsl.search import Search
from django.core.cache import cache
from dongtai_common.models.agent import IastAgent
import uuid


@registry.register_document
class IastAssetVulnerabilityDocument(Document):
    # from asset_vul table
    vul_name = fields.TextField(attr="asset_vul.vul_name")
    vul_detail = fields.TextField(attr="asset_vul.vul_detail")
    license = fields.TextField(attr="asset_vul.license")
    license_level = fields.IntegerField(attr="asset_vul.license_level")
    aql = fields.TextField(attr="asset_vul.aql")
    package_hash = fields.TextField(attr="asset_vul.package_hash")
    package_version = fields.TextField(attr="asset_vul.package_version")
    package_safe_version = fields.TextField(attr="asset_vul.package_safe_version")
    package_latest_version = fields.TextField(attr="asset_vul.package_latest_version")
    package_language = fields.TextField(attr="asset_vul.package_language")
    vul_cve_nums = fields.TextField(attr="asset_vul.vul_cve_nums")
    vul_serial = fields.TextField(attr="asset_vul.vul_serial")
    cve_code = fields.TextField(attr="asset_vul.cve_code")
    have_article = fields.IntegerField(attr="asset_vul.have_article")
    have_poc = fields.IntegerField(attr="asset_vul.have_poc")
    cve_id = fields.IntegerField(attr="asset_vul.cve_id")
    update_time = fields.IntegerField(attr="asset_vul.update_time")
    create_time = fields.IntegerField(attr="asset_vul.create_time")
    update_time_desc = fields.IntegerField(attr="asset_vul.update_time_desc")
    vul_publish_time = fields.DateField(attr="asset_vul.vul_publish_time")
    vul_update_time = fields.DateField(attr="asset_vul.vul_update_time")
    level_id = fields.IntegerField(attr="asset_vul.level_id")

    # from asset_vul_relation
    asset_vul_relation_id = fields.IntegerField(attr="id")
    asset_vul_id = fields.IntegerField(attr="asset_vul_id")
    asset_vul_relation_is_del = fields.IntegerField(attr="is_del")

    # from asset
    asset_user_id = fields.IntegerField(attr="asset.user_id")
    asset_agent_id = fields.IntegerField(attr="asset.agent_id")
    asset_project_id = fields.IntegerField(attr="asset.project_id")
    asset_project_version_id = fields.IntegerField(attr="asset.project_version_id")

    def prepare_vul_cve_nums(self, instance):
        import json
        return json.dumps(instance.asset_vul.vul_cve_nums)

    def generate_id(self, object_instance):
        return object_instance.id

    def get_instances_from_related(self, related_instance):
        """If related_models is set, define how to retrieve the Car instance(s) from the related model.
        The related_models option should be used with caution because it can lead in the index
        to the updating of a lot of items.
        """
        if isinstance(related_instance, IastAgent):
            if related_instance.bind_project_id < 0:
                return IastVulAssetRelation.objects.filter(
                    asset__agent__id=related_instance.pk).all()

    @classmethod
    def search(cls, using=None, index=None):
        uuid_key = uuid.uuid4().hex
        cache_uuid_key = cache.get_or_set(
            f'es-documents-shards-{cls.__name__}', uuid_key, 60 * 1)
        return Search(using=cls._get_using(using),
                      index=cls._default_index(index),
                      doc_type=[cls],
                      model=cls.django.model).params(preference=cache_uuid_key)

    class Index:
        name = ASSET_VUL_INDEX

    class Django:
        model = IastVulAssetRelation
        ignore_signals = False
        auto_refresh = False
