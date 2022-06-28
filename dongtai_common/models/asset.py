#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/8/20 15:10
# software: PyCharm
# project: dongtai-models

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


class Asset(models.Model):
    package_name = models.CharField(max_length=255, blank=True, null=True)
    package_path = models.CharField(max_length=255, blank=True, null=True)
    signature_algorithm = models.CharField(max_length=255, blank=True, null=True)
    signature_value = models.CharField(max_length=255, blank=True, null=True)
    dt = models.IntegerField(blank=True, null=True)
    version = models.CharField(max_length=255, blank=True, null=True)
    safe_version = models.CharField(max_length=255, blank=True, null=False, default='')
    last_version = models.CharField(max_length=255, blank=True, null=False, default='')
    level = models.ForeignKey(IastVulLevel, models.DO_NOTHING, blank=True, null=True, default=4)
    vul_count = models.IntegerField(blank=True, null=True)
    vul_critical_count = models.IntegerField(default=0, blank=True, null=False)
    vul_high_count = models.IntegerField(default=0, blank=True, null=False)
    vul_medium_count = models.IntegerField(default=0, blank=True, null=False)
    vul_low_count = models.IntegerField(default=0, blank=True, null=False)
    vul_info_count = models.IntegerField(default=0, blank=True, null=False)
    agent = models.ForeignKey(
        to=IastAgent,
        on_delete=models.DO_NOTHING,
        related_name='assets',
        related_query_name='asset',
        verbose_name=_('agent'),
        blank=True,
        null=True,
        default=-1
    )
    project = models.ForeignKey(IastProject, on_delete=models.DO_NOTHING, blank=True, null=False, default=-1)
    project_version = models.ForeignKey(IastProjectVersion, on_delete=models.DO_NOTHING, blank=True, null=False,
                                        default=-1)
    user = models.ForeignKey(User, models.DO_NOTHING, null=False, default=-1)
    project_name = models.CharField(max_length=255, blank=True, null=False, default='')
    language = models.CharField(max_length=32, blank=True, null=False, default='')
    license = models.CharField(max_length=64, blank=True, null=False, default='')
    dependency_level = models.IntegerField(null=False, default=0)
    parent_dependency_id = models.IntegerField(blank=True, null=False, default=0)
    is_del = models.SmallIntegerField(blank=True, null=False, default=0)

    # 部门id
    department = models.ForeignKey(Department, models.DO_NOTHING, blank=True, null=True, default=-1)
    # 租户id
    talent = models.ForeignKey(Talent, models.DO_NOTHING, blank=True, null=True, default=-1)

    class Meta:
        managed = get_managed()
        db_table = 'iast_asset'

from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from dongtai_web.utils import get_model_field
from django.db.models.fields.related import ForeignKey
from django_elasticsearch_dsl import Document, fields
from dongtai_conf.settings import ASSET_INDEX 


@registry.register_document
class IastAssetDocument(Document):
    user_id = fields.IntegerField(attr="user_id")
    agent_id = fields.IntegerField(attr="agent_id")
    level_id = fields.IntegerField(attr="level_id")
    project_id = fields.IntegerField(attr="project_id")
    project_version_id = fields.IntegerField(
        attr="project_version_id")
    department_id = fields.IntegerField(attr="department_id")
    talent_id = fields.IntegerField(attr="talent_id")

    def generate_id(self, object_instance):
        return object_instance.id


    class Index:
        name = ASSET_INDEX

    class Django:
        model = Asset
        fields = [
            'id', 'package_name', 'package_path', 'signature_algorithm',
            'signature_value', 'dt', 'version', 'safe_version', 'last_version',
            'vul_count', 'vul_critical_count', 'vul_high_count',
            'vul_medium_count', 'vul_low_count', 'vul_info_count',
            'project_name', 'language', 'license', 'dependency_level',
            'parent_dependency_id', 'is_del'
        ]

        ignore_signals = False
