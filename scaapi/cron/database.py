#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/8/25 11:09
# software: PyCharm
# project: sca

import time

from peewee import *

from webapi.settings import DATABASES

database = MySQLDatabase(
    DATABASES['default']['NAME'], **{
        'charset': DATABASES['default']['OPTIONS']['charset'],
        'sql_mode': 'PIPES_AS_CONCAT',
        'use_unicode': True,
        'host': DATABASES['default']['HOST'],
        'port': int(DATABASES['default']['PORT']),
        'user': DATABASES['default']['USER'],
        'password': DATABASES['default']['PASSWORD']
    })


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class MavenDb(BaseModel):
    atrifact_id = CharField(null=True)
    group_id = CharField(null=True)
    sha_1 = CharField(null=True)
    version = CharField(null=True)
    package_name = CharField(null=True)
    aql = CharField(null=True)

    class Meta:
        table_name = 'sca_maven_db'


class ArtifactDb(BaseModel):
    artifact_id = CharField(null=True)
    component_name = CharField(null=True)
    cve_id = CharField(null=True)
    cwe_id = CharField(null=True)
    dt = IntegerField(null=True, default=int(time.time()))
    group_id = CharField(null=True)
    latest_version = CharField(null=True)
    overview = TextField(null=True)
    stage = CharField(null=True)
    teardown = TextField(null=True)
    title = CharField(null=True)
    reference = CharField(null=True)
    cvss_score = CharField(null=True)
    cvss3_score = CharField(null=True)
    level = CharField(null=True)

    class Meta:
        table_name = 'sca_artifact_db'


class MavenArtifact(BaseModel):
    aid = IntegerField(null=True)
    cph = CharField(null=True)
    dt = IntegerField(null=True, default=int(time.time()))
    safe_version = CharField(null=True)
    version_range = CharField(null=True)
    patch = CharField(null=True)
    cph_version = CharField(null=True)
    type = CharField(null=True)
    group_id = CharField(null=True)
    artifact_id = CharField(null=True)
    version = CharField(null=True)
    signature = CharField(null=True)
    package_name = CharField(null=True)

    class Meta:
        table_name = 'sca_maven_artifact'


class ScaVulDb(BaseModel):
    aql = CharField(null=True)
    cve = CharField(null=True)
    cve_href = CharField(null=True)
    cwe = CharField(null=True)
    cwe_href = CharField(null=True)
    dt = IntegerField(null=True, default=int(time.time()))
    latest_version = CharField(null=True)
    overview = CharField(null=True)
    package_type = CharField(null=True)
    source = CharField(null=True)
    teardown = CharField(null=True)
    url = CharField(null=True)
    version_condition = CharField(null=True)
    version_range = CharField(null=True)
    vul_level = CharField(null=True)
    vul_name = CharField(null=True)
    extra = CharField(null=True)

    class Meta:
        table_name = 'sca_vul_db'


class ScaRecord(BaseModel):
    page = IntegerField(null=False)
    total = IntegerField(null=False)
    dt = IntegerField(null=False)
    type = CharField(null=False)
    data = CharField(null=True)

    class Meta:
        table_name = 'sca_record'
