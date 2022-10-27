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


from _typeshed import Incomplete
class HttpMethod(models.Model):
    method: Incomplete = models.CharField(max_length=100, blank=True)

    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'iast_http_method'


class IastApiMethod(models.Model):
    method: Incomplete = models.CharField(max_length=100, blank=True)
    http_method: Incomplete = models.ManyToManyField(
        HttpMethod, blank=True, through='IastApiMethodHttpMethodRelation')

    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'iast_api_methods'


class IastApiMethodHttpMethodRelation(models.Model):
    api_method: Incomplete = models.ForeignKey(IastApiMethod,
                                   on_delete=models.CASCADE,
                                   db_constraint=False,
                                   db_column='api_method_id')
    http_method: Incomplete = models.ForeignKey(HttpMethod,
                                    on_delete=models.CASCADE,
                                    db_constraint=False,
                                    db_column='http_method_id')

    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'iast_http_method_relation'
        unique_together: Incomplete = ['api_method_id', 'http_method_id']
class FromWhereChoices(models.IntegerChoices):
    FROM_AGENT: int = 1
    FROM_METHOD_POOL: int = 2


class IastApiRoute(models.Model):
    path: Incomplete = models.CharField(max_length=255, blank=True)
    code_class: Incomplete = models.CharField(max_length=255,
                                  blank=True,
                                  db_column='code_class')
    description: Incomplete = models.CharField(max_length=500, blank=True)
    method: Incomplete = models.ForeignKey(IastApiMethod,
                               on_delete=models.DO_NOTHING,
                               db_constraint=False,
                               db_index=True,
                               db_column='method_id')
    code_file: Incomplete = models.CharField(max_length=500,
                                 blank=True,
                                 db_column='code_file')
    controller: Incomplete = models.CharField(max_length=100, blank=True)
    agent: Incomplete = models.ForeignKey(IastAgent,
                              on_delete=models.CASCADE,
                              db_constraint=False,
                              db_index=True,
                              db_column='agent_id')
    from_where: Incomplete = models.IntegerField(default=FromWhereChoices.FROM_AGENT,
                                     choices=FromWhereChoices.choices)
    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'iast_api_route'
        unique_together: Incomplete = ['path', 'method']


class IastApiParameter(models.Model):
    name: Incomplete = models.CharField(max_length=100, blank=True)
    parameter_type: Incomplete = models.CharField(max_length=100,
                                      blank=True,
                                      default='',
                                      db_column='type')
    annotation: Incomplete = models.CharField(max_length=500, blank=True)
    route: Incomplete = models.ForeignKey(IastApiRoute,
                              on_delete=models.CASCADE,
                              db_constraint=False,
                              db_index=True,
                              db_column='route_id')

    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'iast_api_parameter'
        unique_together: Incomplete = ['name', 'route_id']


class IastApiResponse(models.Model):
    return_type: Incomplete = models.CharField(max_length=100, blank=True)
    route: Incomplete = models.ForeignKey(IastApiRoute,
                              on_delete=models.CASCADE,
                              db_constraint=False,
                              db_index=True,
                              db_column='route_id')

    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'iast_api_response'
        unique_together: Incomplete = ['return_type', 'route_id']
