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
from rest_framework.serializers import Serializer


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

from rest_framework.serializers import SerializerMetaclass
def extend_schema_with_envcheck(querys: list = [], request_body: list = []):
    def myextend_schema(func):
        import os
        if os.getenv('environment', None) == 'TEST':
            from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiTypes
            parameters = list(filter(lambda x: x, map(_filter_query, querys)))
            deco = extend_schema(
                parameters=parameters,
                examples=[OpenApiExample('Example1', value=request_body)],
                request={'application/json': OpenApiTypes.OBJECT},
            )
            funcw = deco(func)
            funcw.querys = parameters
            funcw.request_body = request_body
            return funcw
        return func
    return myextend_schema


def _filter_query(item):
    from drf_spectacular.utils import OpenApiParameter
    if isinstance(item, SerializerMetaclass):
        return item
    elif isinstance(item, dict):
        return OpenApiParameter(**item)


def batch_queryset(queryset, batch_size=1):
    iter_ = 0
    while True:
        queryset_ = list(queryset[iter_:iter_ + 1])
        iter_ += 1
        if not queryset_:
            break
        else:
            yield queryset_[0]


def checkcover(api_route, agents, http_method=None):
    uri_hash = hashlib.sha1(api_route.path.encode('utf-8')).hexdigest()
    api_method_id = api_route.method_id
    q = Q(agent_id__in=[_['id'] for _ in agents])
    if http_method:
        http_method_ids = IastApiMethodHttpMethodRelation.objects.filter(
            api_method_id=api_method_id).values('api_method_id')
        http_methods = HttpMethod.objects.filter(
            pk__in=http_method_ids).all().values_list('method')
        q = q & Q(http_method__in=http_methods)
    q = q & Q(uri_sha1=uri_hash)
    if MethodPool.objects.filter(q)[0:1]:
        return True
    return False


def sha1(string, encoding='utf-8'):
    return hashlib.sha1(string.encode(encoding)).hexdigest()
