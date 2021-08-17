#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/8/26 16:00
# software: PyCharm
# project: dongtai-models
from django.db import models

from dongtai.models.sca_artifact_db import ScaArtifactDb
from dongtai.utils.settings import get_managed


class ScaMavenArtifact(models.Model):
    aid = models.ForeignKey(ScaArtifactDb, models.DO_NOTHING, db_column='aid', blank=True, null=True)
    safe_version = models.CharField(max_length=255, blank=True, null=True)
    version_range = models.CharField(max_length=255, blank=True, null=True)
    cph_version = models.CharField(max_length=255, blank=True, null=True)
    dt = models.IntegerField(blank=True, null=True)
    patch = models.CharField(max_length=255, blank=True, null=True)
    cph = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    group_id = models.CharField(max_length=255, blank=True, null=True)
    artifact_id = models.CharField(max_length=255, blank=True, null=True)
    version = models.CharField(max_length=255, blank=True, null=True)
    signature = models.CharField(max_length=255, blank=True, null=True)
    package_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = get_managed()
        db_table = 'sca_maven_artifact'
        unique_together = (('cph_version', 'aid'),)
