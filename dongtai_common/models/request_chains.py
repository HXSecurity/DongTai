######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : request_chains
# @created     : 星期四 12月 09, 2021 12:17:18 CST
#
# @description :
######################################################################


from django.db import models

from dongtai_common.models.agent import IastAgent
from dongtai_common.models.agent_method_pool import MethodPool
from dongtai_common.models.project import IastProject
from dongtai_common.models.project_version import IastProjectVersion
from dongtai_common.utils.db import get_timestamp
from dongtai_common.utils.settings import get_managed


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
    stack = models.TextField(blank=True, null=True)  # This field type is a guess.
    project_path = models.CharField(max_length=255, blank=True, null=True, default="")
    parent_project_id = models.IntegerField(blank=True, default=-1)
    url = models.CharField(max_length=255, blank=True, null=True)
    request = models.TextField(blank=True, null=True)  # This field type is a guess.
    response = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = get_managed()
        db_table = "iast_request_chains_vul_context"


class IastAgentRequestChainsTopoGraph(models.Model):
    start_project = models.ForeignKey(
        IastProject,
        models.DO_NOTHING,
        blank=True,
        default=-1,
        db_constraint=False,
    )
    start_project_version = models.ForeignKey(
        IastProjectVersion,
        models.DO_NOTHING,
        blank=True,
        default=-1,
        db_constraint=False,
    )
    graph_hash = models.CharField(
        max_length=255,
        blank=True,
        unique=True,
    )
    dot_string = models.TextField()
    max_depth = models.IntegerField()

    class Meta:
        managed = get_managed()
        db_table = "iast_request_chains_topo_graph"


class IastAgentRequestChainsTopoGraphVec(models.Model):
    graph_hash = models.ForeignKey(
        IastAgentRequestChainsTopoGraph,
        max_length=255,
        blank=True,
        to_field="graph_hash",
        on_delete=models.CASCADE,
        db_constraint=False,
    )
    level_id = models.IntegerField()
    source_project_version = models.ForeignKey(
        IastProjectVersion,
        models.DO_NOTHING,
        blank=True,
        default=-1,
        db_constraint=False,
        related_name="source_project_version",
    )
    target_project_version = models.ForeignKey(
        IastProjectVersion,
        models.DO_NOTHING,
        blank=True,
        default=-1,
        db_constraint=False,
        related_name="target_project_version",
    )
    source_project = models.ForeignKey(
        IastProject,
        models.DO_NOTHING,
        blank=True,
        default=-1,
        db_constraint=False,
        related_name="source_project",
    )
    target_project = models.ForeignKey(
        IastProject,
        models.DO_NOTHING,
        blank=True,
        default=-1,
        db_constraint=False,
        related_name="target_project",
    )
    source_node_tag = models.CharField(
        max_length=255,
        blank=True,
    )
    target_node_tag = models.CharField(
        max_length=255,
        blank=True,
    )
    expandable = models.BooleanField(default=False)

    class Meta:
        managed = get_managed()
        db_table = "iast_request_chains_topo_graph_vecs"
        unique_together = (("graph_hash", "source_node_tag", "target_node_tag"),)


class IastAgentRequestChainsTotalProjectVersionGraphVec(models.Model):
    source_project_version = models.ForeignKey(
        IastProjectVersion,
        models.DO_NOTHING,
        blank=True,
        default=-1,
        db_constraint=False,
        related_name="total_source_project_version",
    )
    target_project_version = models.ForeignKey(
        IastProjectVersion,
        models.DO_NOTHING,
        blank=True,
        default=-1,
        db_constraint=False,
        related_name="total_target_project_version",
    )

    class Meta:
        managed = get_managed()
        db_table = "iast_request_chains_total_project_version_graph_vec"
        unique_together = (("source_project_version", "target_project_version"),)


class IastAgentRequestChainsTotalProjectGraphVec(models.Model):
    source_project = models.ForeignKey(
        IastProject,
        models.DO_NOTHING,
        blank=True,
        default=-1,
        db_constraint=False,
        related_name="total_source_project",
    )
    target_project = models.ForeignKey(
        IastProject,
        models.DO_NOTHING,
        blank=True,
        default=-1,
        db_constraint=False,
        related_name="total_target_project",
    )

    class Meta:
        managed = get_managed()
        db_table = "iast_request_chains_total_project_graph_vec"
        unique_together = (("source_project", "target_project"),)


class IastAgentRequestChainsTopoTotalProjectVersionGraph(models.Model):
    graph_hash = models.CharField(
        max_length=255,
        blank=True,
        unique=True,
    )
    dot_string = models.TextField()

    class Meta:
        managed = get_managed()
        db_table = "iast_request_chains_topo_total_project_version_graph"


class IastAgentRequestChainsTopoTotalProjectVersionGraphVec(models.Model):
    total_project_version_graph = models.ForeignKey(
        IastAgentRequestChainsTopoTotalProjectVersionGraph,
        max_length=255,
        blank=True,
        to_field="graph_hash",
        on_delete=models.CASCADE,
        db_constraint=False,
    )
    source_project_version = models.ForeignKey(
        IastProjectVersion,
        models.DO_NOTHING,
        blank=True,
        default=-1,
        db_constraint=False,
        related_name="total_source_project_version_node",
    )
    target_project_version = models.ForeignKey(
        IastProjectVersion,
        models.DO_NOTHING,
        blank=True,
        default=-1,
        db_constraint=False,
        related_name="total_target_project_version_node",
    )

    class Meta:
        managed = get_managed()
        db_table = "iast_request_chains_topo_total_project_version_graph_vec"
        unique_together = (("total_project_version_graph", "source_project_version", "target_project_version"),)


class IastAgentRequestChainsTopoTotalProjectVersionGraphProjectRel(models.Model):
    total_project_version_graph = models.ForeignKey(
        IastAgentRequestChainsTopoTotalProjectVersionGraph,
        max_length=255,
        blank=True,
        to_field="graph_hash",
        on_delete=models.CASCADE,
        db_constraint=False,
    )
    project_version = models.ForeignKey(
        IastProjectVersion,
        models.DO_NOTHING,
        blank=True,
        default=-1,
        db_constraint=False,
        db_index=True,
    )

    class Meta:
        managed = get_managed()
        db_table = "iast_request_chains_topo_total_project_version_graph_rel"
        unique_together = (("total_project_version_graph", "project_version"),)
