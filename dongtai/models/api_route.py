######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : api_route
# @created     : Tuesday Aug 17, 2021 17:43:27 CST
#
# @description :
######################################################################

from django.db import models
from dongtai.utils.settings import get_managed


class ApiRoute(models.Model):
    path = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=500, blank=True)
    method = models.CharField(max_length=100, blank=True)
    file_ = models.CharField(max_length=500, blank=True, db_column='file')
    controller = models.CharField(max_length=100, blank=True)

    class Meta:
        managed = get_managed()
        db_table = 'iast_api_route'


class ApiParameter(models.Model):
    name = models.CharField(max_length=100, blank=True)
    type_ = models.CharField(max_length=100, blank=True, db_column='type')
    annotation = models.CharField(max_length=500, blank=True)
    route_id = models.ForeignKey(ApiRoute,
                                 on_delete=models.CASCADE,
                                 db_constraint=False)

    class Meta:
        managed = get_managed()
        db_table = 'iast_api_parameter'


class ApiResponse(models.Model):
    return_type = models.CharField(max_length=100, blank=True)
    route_id = models.ForeignKey(ApiRoute,
                                 on_delete=models.CASCADE,
                                 db_constraint=False)

    class Meta:
        managed = get_managed()
        db_table = 'iast_api_response'
