#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/8/24 15:20
# software: PyCharm
# project: sca
from django.db import models


class ScaMavenArtifact(models.Model):
    # aid = models.ForeignKey(ScaArtifactDb, models.DO_NOTHING, db_column='aid', related_name='vul', blank=True, null=True)
    aid = models.IntegerField(blank=True, null=True)
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
        managed = False
        db_table = 'sca_maven_artifact'
        unique_together = (('cph_version', 'aid'),)
