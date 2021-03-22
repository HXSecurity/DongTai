#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/19 上午10:47
# software: PyCharm
# project: lingzhi-webapi
from django.db import models


class IastAgentProperties(models.Model):
    hook_type = models.IntegerField(blank=True, null=True)
    dump_class = models.IntegerField(blank=True, null=True)
    create_time = models.IntegerField(blank=True, null=True)
    update_time = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    agent_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'iast_agent_properties'
