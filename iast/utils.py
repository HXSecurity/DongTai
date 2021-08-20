#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:Bidaya0
# datetime:2021/7/27 12:06
# software: Vim8
# project: webapi

from functools import reduce
from django.db.models import Q
import operator
import hashlib
from dongtai.models.api_route import IastApiRoute, IastApiMethod, IastApiRoute, HttpMethod, IastApiResponse, IastApiMethodHttpMethodRelation
from dongtai.models.agent_method_pool import MethodPool


def get_model_field(model, exclude=[], include=[]):
    fields = [field.name for field in model._meta.fields]
    if include:
        return [
            field for field in list(set(fields) - set(exclude))
            if field in include
        ]
    return list(set(fields) - set(exclude))


def assemble_query(condictions: dict,
                   lookuptype='',
                   base_query=Q(),
                   operator_=operator.or_):
    return reduce(
        operator_,
        map(
            lambda x: Q(**x),
            map(
                lambda kv_pair: {
                    '__'.join(filter(lambda x: x, [kv_pair[0], lookuptype])):
                        kv_pair[1]
                }, condictions)), base_query)


def extend_schema_with_envcheck(querys, request_body):
    def myextend_schema(func):
        import os
        if os.getenv('environment', None) == 'TEST':
            from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiTypes
            deco = extend_schema(
                parameters=[OpenApiParameter(**query) for query in querys],
                examples=[OpenApiExample('Example1', value=request_body)],
                request={'application/json': OpenApiTypes.OBJECT},
            )
            funcw = deco(func)
            funcw.querys = querys
            funcw.reqbody = request_body
            return funcw
        return func

    return myextend_schema

def batch_queryset(queryset, batch_size=1):
    iter_ = 0
    while True:
        queryset = list(queryset[iter_:iter_ + 1])
        if not queryset:
            break
        else:
            yield queryset[0]


def checkcover(api_route, agents, http_method):
    uri_hash = hashlib.sha1(api_route.uri.encode('utf-8')).hexdigest()
    api_method_id = api_route.values('method_id')
    http_method_ids = IastApiMethodHttpMethodRelation.objects.filter(
        api_method_id=api_method_id).values('api_method_id')
    http_methods = HttpMethod.objects.filter(
        http_method_ids__in=http_method_ids).all().values_list('method')
    q = Q(agent_id__in=[_['id'] for _ in agents])
    q = q & Q(http_method__in=http_methods)
    q = q & Q(uri_hash=uri_hash)
    if MethodPool.objects.filter(q)[0:1]:
        return True
    return False
