#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/8/24 15:21
# software: PyCharm
# project: sca
from django.db import models


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
    reference = models.CharField(max_length=2000, blank=True, null=True)
    dt = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sca_artifact_db'
        unique_together = (('cve_id', 'group_id', 'artifact_id', 'latest_version'),)
