######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : request_chains
# @created     : 星期四 12月 09, 2021 12:17:18 CST
#
# @description :
######################################################################

from django.db import models
from django.utils.translation import gettext_lazy as _
from dongtai_common.utils.settings import get_managed
from dongtai_common.models.agent_method_pool import MethodPool
from dongtai_common.models.project import IastProject
from dongtai_common.models.agent import IastAgent
import time
from dongtai_common.utils.db import get_timestamp


class IastAgentRequestChains(models.Model):
    request_hash = models.CharField(max_length=255, blank=True, null=True)
    span_id = models.CharField(max_length=255, blank=True, null=True)
    parent_span_id = models.CharField(max_length=255, blank=True, null=True)
    protocol = models.CharField(max_length=255, blank=True, null=True)
    source = models.ForeignKey(
        MethodPool, models.DO_NOTHING, blank=True, default=-1, db_constraint=False, related_name="source"
    )
    target = models.ForeignKey(
        MethodPool, models.DO_NOTHING, blank=True, default=-1, db_constraint=False, related_name="target"
    )
    project = models.ForeignKey(IastProject, models.DO_NOTHING, blank=True, default=-1, db_constraint=False)
    source_agent = models.ForeignKey(
        IastAgent, models.DO_NOTHING, blank=True, default=-1, db_constraint=False, related_name="source_agent"
    )
    target_agent = models.ForeignKey(
        IastAgent, models.DO_NOTHING, blank=True, default=-1, db_constraint=False, related_name="target_agent"
    )
    level_id = models.IntegerField(blank=True, default=0)
    dt = models.IntegerField(blank=True, default=get_timestamp)

    class Meta:
        managed = get_managed()
        db_table = "iast_request_chains"


class IastAgentRequestChainsVulContext(models.Model):
    vul_id = models.IntegerField(blank=True, default=0)
    project = models.ForeignKey(IastProject, models.DO_NOTHING, blank=True, default=-1, db_constraint=False)
    method_pool_id = models.IntegerField(blank=True, default=0)
    level_id = models.IntegerField(blank=True, default=0)
    request_hash = models.CharField(max_length=255, blank=True, null=True)
    #    span_id = models.CharField(max_length=255, blank=True, null=True)
    #    parent_span_id = models.CharField(max_length=255, blank=True, null=True)
    stack = models.TextField(blank=True, null=True)  # This field type is a guess.
    project_path = models.CharField(max_length=255, blank=True, null=True, default="")
    parent_project_id = models.IntegerField(blank=True, default=-1)
    url = models.CharField(max_length=255, blank=True, null=True)
    request = models.TextField(blank=True, null=True)  # This field type is a guess.
    response = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = get_managed()
        db_table = "iast_request_chains_vul_context"
