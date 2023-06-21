######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : api_route
# @created     : Tuesday Aug 17, 2021 17:43:27 CST
#
# @description :
######################################################################

from django.db import models
from dongtai_common.utils.settings import get_managed
from dongtai_common.models.agent import IastAgent
from dongtai_common.models.project import IastProject
from dongtai_common.models.project_version import IastProjectVersion


class FromWhereChoices(models.IntegerChoices):
    FROM_AGENT = 1


class IastApiRouteV2(models.Model):
    path = models.CharField(max_length=255, blank=True)
    method = models.CharField(max_length=100, blank=True)
    from_where = models.IntegerField(default=FromWhereChoices.FROM_AGENT,
                                     choices=FromWhereChoices.choices)
    project = models.ForeignKey(IastProject,
                                on_delete=models.CASCADE,
                                blank=True,
                                null=True,
                                default=-1)
    project_version = models.ForeignKey(IastProjectVersion,
                                        on_delete=models.CASCADE,
                                        blank=True,
                                        null=True,
                                        default=-1)
    is_cover = models.IntegerField(default=0)
    api_info = models.JSONField(blank=True, null=True, default=dict)

    class Meta:
        managed = get_managed()
        db_table = 'iast_api_route_v2'
