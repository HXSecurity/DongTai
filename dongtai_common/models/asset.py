#!/usr/bin/env python
# datetime:2020/8/20 15:10

import uuid

from django.core.cache import cache
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from django_elasticsearch_dsl.search import Search

from dongtai_common.models import User
from dongtai_common.models.agent import IastAgent
from dongtai_common.models.department import Department
from dongtai_common.models.project import IastProject
from dongtai_common.models.project_version import IastProjectVersion
from dongtai_common.models.talent import Talent
from dongtai_common.models.vul_level import IastVulLevel
from dongtai_common.utils.settings import get_managed
from dongtai_conf.settings import ASSET_INDEX


class Asset(models.Model):
    id = models.BigAutoField(primary_key=True)
    package_name = models.CharField(max_length=255, blank=True)
    package_path = models.CharField(max_length=255, blank=True)
    signature_algorithm = models.CharField(max_length=255, blank=True)
    signature_value = models.CharField(max_length=255, blank=True)
    dt = models.IntegerField()
    version = models.CharField(max_length=255, blank=True)
    safe_version = models.CharField(max_length=255, blank=True)
    last_version = models.CharField(max_length=255, blank=True)
    level = models.ForeignKey(IastVulLevel, models.DO_NOTHING, default=4)
    vul_count = models.IntegerField()
    vul_critical_count = models.IntegerField(default=0)
    vul_high_count = models.IntegerField(default=0)
    vul_medium_count = models.IntegerField(default=0)
    vul_low_count = models.IntegerField(default=0)
    vul_info_count = models.IntegerField(default=0)
    agent = models.ForeignKey(
        to=IastAgent,
        on_delete=models.CASCADE,
        related_name="assets",
        related_query_name="asset",
        verbose_name=_("agent"),
        default=-1,
    )
    project = models.ForeignKey(IastProject, on_delete=models.CASCADE, default=-1)
    project_version = models.ForeignKey(IastProjectVersion, on_delete=models.CASCADE, default=-1)
    user = models.ForeignKey(User, models.DO_NOTHING, default=-1)
    project_name = models.CharField(max_length=255, blank=True)
    language = models.CharField(max_length=32, blank=True)
    license = models.CharField(max_length=64, blank=True)
    dependency_level = models.IntegerField(default=0)
    parent_dependency_id = models.IntegerField(default=0)
    is_del = models.SmallIntegerField(default=0)

    # 部门id
    department = models.ForeignKey(Department, models.DO_NOTHING, default=-1)
    # 租户id
    talent = models.ForeignKey(Talent, models.DO_NOTHING, default=-1)
    safe_version_list = models.JSONField(default=list)
    nearest_safe_version = models.JSONField(default=str)
    latest_safe_version = models.JSONField(default=str)
    license_list = models.JSONField(default=list)
    highest_license = models.JSONField(default=dict)

    class Meta:
        managed = get_managed()
        db_table = "iast_asset"


@registry.register_document
class IastAssetDocument(Document):
    user_id = fields.IntegerField(attr="user_id")
    agent_id = fields.IntegerField(attr="agent_id")
    level_id = fields.IntegerField(attr="level_id")
    project_id = fields.IntegerField(attr="project_id")
    project_version_id = fields.IntegerField(attr="project_version_id")
    department_id = fields.IntegerField(attr="department_id")
    talent_id = fields.IntegerField(attr="talent_id")
    safe_version_list = fields.ObjectField()
    nearest_safe_version = fields.ObjectField()
    latest_safe_version = fields.ObjectField()
    license_list = fields.ObjectField()
    highest_license = fields.ObjectField()

    def generate_id(self, object_instance):
        return object_instance.id

    def prepare_safe_version_list(self, object_instance):
        return object_instance.safe_version_list

    def prepare_nearest_safe_version(self, object_instance):
        return object_instance.nearest_safe_version

    def prepare_latest_safe_version(self, object_instance):
        return object_instance.latest_safe_version

    def prepare_license_list(self, object_instance):
        return object_instance.license_list

    def prepare_highest_license(self, object_instance):
        return object_instance.highest_license

    @classmethod
    def search(cls, using=None, index=None):
        uuid_key = uuid.uuid4().hex
        cache_uuid_key = cache.get_or_set(f"es-documents-shards-{cls.__name__}", uuid_key, 60 * 1)
        return Search(
            using=cls._get_using(using),
            index=cls._default_index(index),
            doc_type=[cls],
            model=cls.django.model,
        ).params(preference=cache_uuid_key)

    def get_instances_from_related(self, related_instance):
        """If related_models is set, define how to retrieve the Car instance(s) from the related model.
        The related_models option should be used with caution because it can lead in the index
        to the updating of a lot of items.
        """
        if isinstance(related_instance, IastAgent):
            if related_instance.bind_project_id < 0:
                return Asset.objects.filter(agent_id=related_instance.pk).all()
            return None
        return None

    class Index:
        name = ASSET_INDEX

    class Django:
        model = Asset
        fields = [
            "id",
            "package_name",
            "package_path",
            "signature_algorithm",
            "signature_value",
            "dt",
            "version",
            "safe_version",
            "last_version",
            "vul_count",
            "vul_critical_count",
            "vul_high_count",
            "vul_medium_count",
            "vul_low_count",
            "vul_info_count",
            "project_name",
            "language",
            "license",
            "dependency_level",
            "parent_dependency_id",
            "is_del",
        ]

        ignore_signals = False
