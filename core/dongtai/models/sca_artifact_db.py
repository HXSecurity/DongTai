#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/8/26 16:02
# software: PyCharm
# project: dongtai-models
from django.db import models
from dongtai.utils.settings import get_managed
from dongtai.utils.customfields import trans_char_field
from typing import Any


class ScaArtifactDb(models.Model):
    cwe_id = models.CharField(max_length=20, blank=True, null=True)
    cve_id = models.CharField(max_length=20, blank=True, null=True)
    stage = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    overview = models.TextField(blank=True, null=True)
    teardown = models.TextField(blank=True, null=True)
    group_id = models.CharField(max_length=256, blank=True, null=True)
    artifact_id = models.CharField(max_length=256, blank=True, null=True)
    latest_version = models.CharField(max_length=50, blank=True, null=True)
    component_name = models.CharField(max_length=512, blank=True, null=True)
    dt = models.IntegerField(blank=True, null=True)
    reference = models.TextField(blank=True, null=True)
    cvss_score = models.FloatField(blank=True, null=True)
    cvss3_score = models.FloatField(blank=True, null=True)
    level = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = get_managed()
        db_table = 'sca_artifact_db'
        unique_together = (('cve_id', 'group_id', 'artifact_id',
                            'latest_version'), )

    @trans_char_field(
        'level', {
            'zh': {
                "无风险": "无风险",
                "低危": "低危",
                "中危": "中危",
                "高危": "高危"
            },
            'en': {
                "无风险": "No risk",
                "低危": "Low",
                "中危": "Medium",
                "高危": "High"
            },
        })
    def __getattribute__(self, name) -> Any:
        return super().__getattribute__(name)
