#!/usr/bin/env python
# -*- coding:utf-8 -*-
# datetime:2021/1/14 下午3:35
from dongtai_conf.settings import METHOD_POOL_INDEX
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from django.db import models
from django.utils.translation import gettext_lazy as _

from dongtai_common.models.agent import IastAgent
from dongtai_common.models.hook_strategy import HookStrategy
from dongtai_common.utils.settings import get_managed

# 'id', 'agent', 'uri', 'http_method', 'http_scheme', 'req_header', 'req_params', 'req_data', 'taint_value','param_name'


class MethodPool(models.Model):
    id = models.BigAutoField(primary_key=True)
    agent = models.ForeignKey(IastAgent, models.DO_NOTHING, db_constraint=False)
    url = models.CharField(max_length=2000, blank=True)
    uri = models.CharField(max_length=2000, blank=True)
    http_method = models.CharField(max_length=10, blank=True)
    http_scheme = models.CharField(max_length=20, blank=True)
    http_protocol = models.CharField(max_length=255, blank=True)
    req_header = models.CharField(max_length=2000, blank=True, null=True)
    req_params = models.CharField(max_length=2000, blank=True, null=True)
    req_data = models.CharField(max_length=4000, blank=True, null=True)
    res_header = models.CharField(max_length=1000, blank=True, null=True)
    res_body = models.TextField(blank=True, null=True)
    req_header_fs = models.TextField(db_column="req_header_for_search")
    context_path = models.CharField(max_length=255, blank=True, null=True)
    method_pool = models.TextField()  # This field type is a guess.
    pool_sign = models.CharField(
        unique=True, blank=True, max_length=40
    )  # This field type is a guess.
    clent_ip = models.CharField(max_length=255, blank=True)
    create_time = models.IntegerField()
    update_time = models.IntegerField()
    uri_sha1 = models.CharField(max_length=40, blank=True, db_index=True)
    sinks = models.ManyToManyField(
        HookStrategy,
        verbose_name=_("sinks"),
        blank=True,
        related_name="method_pools",
        related_query_name="method_pool",
    )

    class Meta:
        managed = get_managed()
        db_table = "iast_agent_method_pool"
        indexes = [models.Index(fields=["uri_sha1", "http_method", "agent"])]


@registry.register_document
class MethodPoolDocument(Document):
    user_id = fields.IntegerField(attr="agent.user_id")
    bind_project_id = fields.IntegerField(attr="agent.bind_project_id")
    project_version_id = fields.IntegerField(attr="agent.project_version_id")
    req_header_for_search = fields.TextField(attr="req_header_fs")
    language = fields.TextField(attr="agent.language")
    agent_id = fields.TextField(attr="agent_id")

    def generate_id(self, object_instance):
        return "-".join([str(object_instance.agent_id), str(object_instance.pool_sign)])

    class Index:
        name = METHOD_POOL_INDEX

    class Django:
        model = MethodPool

        fields = [
            "res_header",
            "uri_sha1",
            "url",
            "update_time",
            "res_body",
            "req_params",
            "req_header",
            "req_data",
            "pool_sign",
            "method_pool",
            "id",
            "http_scheme",
            "http_protocol",
            "http_method",
            "create_time",
            "context_path",
            "clent_ip",
        ]

        ignore_signals = False
