#!/usr/bin/env python
# datetime:2021/1/14 下午2:54
from django.db import models

from dongtai_common.models.agent import IastAgent
from dongtai_common.utils.settings import get_managed


class IastAgentProperties(models.Model):
    hook_type = models.IntegerField(blank=True, null=True)
    dump_class = models.IntegerField(blank=True, null=True)
    create_time = models.IntegerField(blank=True, null=True)
    update_time = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    agent = models.ForeignKey(IastAgent, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = get_managed()
        db_table = "iast_agent_properties"
