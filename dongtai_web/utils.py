#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:Bidaya0
# datetime:2021/7/27 12:06
# software: Vim8
# project: webapi

from dongtai_common.models.profile import IastProfile
from requests.exceptions import ConnectionError, ConnectTimeout
import logging
import json
import requests
from urllib.parse import urlparse
import uuid
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.utils.text import format_lazy
from rest_framework.serializers import SerializerMetaclass
from functools import reduce
from django.db.models import Q
import operator
import hashlib
from dongtai_common.models.api_route import HttpMethod, IastApiMethodHttpMethodRelation
from dongtai_common.models.agent_method_pool import MethodPool
from dongtai_common.models.vulnerablity import IastVulnerabilityModel
from dongtai_conf.settings import OPENAPI
from typing import List, Dict, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from django.db.models.query import QuerySet, ValuesQuerySet


def get_model_field(model, exclude=[], include=[]):
    fields = [field.name for field in model._meta.fields]
    if include:
        return [
            field for field in list(set(fields) - set(exclude))
            if field in include
        ]
    return list(set(fields) - set(exclude))


def get_model_order_options(*args, **kwargs):
    order_fields = get_model_field(*args, **kwargs)
    return order_fields + list(map(lambda x: ''.join(['-', x]), order_fields))

# temporary fit in to cython
# def assemble_query(condictions: List,


def assemble_query(condictions: list,
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


def assemble_query_2(condictions: list,
                     lookuptype='',
                     base_query=Q(),
                     operator_=operator.or_):
    return reduce(
        operator_,
        map(
            lambda x: ~Q(**x),
            map(
                lambda kv_pair: {
                    '__'.join(filter(lambda x: x, [kv_pair[0], lookuptype])):
                    kv_pair[1]
                }, condictions)), base_query)


def extend_schema_with_envcheck(querys: list = [],
                                request_bodys: Union[List, Dict] = [],
                                response_bodys: list = [],
                                response_schema=None,
                                **kwargs):
    def myextend_schema(func):
        import os
        if os.getenv(
            'environment',
            None) in (
            'TEST',
            'DOC') or os.getenv(
            'DOC',
                None) == 'TRUE':
            from drf_spectacular.utils import extend_schema, OpenApiTypes
            from drf_spectacular.utils import OpenApiResponse
            parameters = list(filter(lambda x: x, map(_filter_query, querys)))
            request_examples = list(
                filter(lambda x: x, map(_filter_request_body, request_bodys)))
            response_examples = list(
                filter(lambda x: x, map(_filter_response_body, response_bodys)))
            examples = request_examples + response_examples
            if kwargs.get('request', None) and request_examples:
                kwargs['request'] = {'application/json': OpenApiTypes.OBJECT}
            elif isinstance(kwargs.get('request', None),
                            SerializerMetaclass):
                kwargs['request'] = {'application/json': kwargs['request']}
            elif kwargs.get('request', None):
                kwargs['request'] = {'application/json': kwargs['request']}
            deco = extend_schema(
                parameters=parameters,
                examples=examples if examples else None,
                responses={
                    200: OpenApiResponse(
                        description=_('The http status codes are both 200, please use the status and msg field returned by the response data to troubleshoot'),  # type: ignore
                        response=response_schema)},
                **kwargs)
            funcw = deco(func)
            funcw.querys = querys
            funcw.request_body = request_bodys if request_bodys else []
            return funcw
        return func

    return myextend_schema


def extend_schema_with_envcheck_v2(*args, **kwargs):

    def myextend_schema(func):
        import os
        if os.getenv('environment', None) in ('TEST', 'DOC') or os.getenv(
                'DOC', None) == 'TRUE':
            from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiTypes
            deco = extend_schema(*args, **kwargs)
            funcw = deco(func)
            return funcw
        return func

    return myextend_schema


def get_response_serializer(data_serializer=None,
                            msg_list=None,
                            status_msg_keypair=None):
    status_msg_keypair = (
        ((201, 'success'),
         'success'), ) if status_msg_keypair is None else status_msg_keypair
    msg_list = list(
        set(map(lambda x: x[1], map(lambda x: x[0], status_msg_keypair))))
    status_list = list(
        set(map(lambda x: x[0], map(lambda x: x[0], status_msg_keypair))))
    msg_list = ['success'] if msg_list is None else msg_list
    status_list = [201] if status_list is None else status_list
    newclass = type(
        str(uuid.uuid1()), (serializers.Serializer, ), {
            'status':
            serializers.IntegerField(default=201,
                                     help_text=format_lazy(
                                         "{} :" + "{} ; " * len(status_list),
                                         *([_("status code")] + status_list))),
            'msg':
            serializers.CharField(
                default='success',
                help_text=format_lazy(
                    "{} :" + "{} ; " * len(msg_list),
                    *([_("human readable message")] + msg_list))),
            'data':
            data_serializer
        })
    return newclass


def _filter_query(item):
    from drf_spectacular.utils import OpenApiParameter
    if isinstance(item, SerializerMetaclass):
        return item
    elif isinstance(item, dict):
        return OpenApiParameter(**item)


def _filter_request_body(item):
    from drf_spectacular.utils import OpenApiExample
    if isinstance(item, dict):
        item['request_only'] = True
        return OpenApiExample(**item)


def _filter_response_body(item):
    from drf_spectacular.utils import OpenApiExample
    if isinstance(item, dict):
        item['response_only'] = True
        return OpenApiExample(**item)


def _map_response_description(item):
    """
    struct like {(1,2):'3'}
    """
    key, value = item
    return "{} : {} : {}".format(key[0], key[1], value)


def _reduce_response_description(itema, itemb):
    return "{} \n{} ".format(itema, itemb)


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
    uri_hash = hashlib.sha1(api_route.path.encode('utf-8'), usedforsecurity=False).hexdigest()
    api_method_id = api_route.method_id
    q = Q(agent_id__in=[_['id'] for _ in agents])
    if http_method:
        http_method_ids = IastApiMethodHttpMethodRelation.objects.filter(
            api_method_id=api_method_id).values('api_method_id')
        http_methods = HttpMethod.objects.filter(
            pk__in=http_method_ids).all().values_list('method')
        q = q & Q(http_method__in=http_methods)
    q = q & Q(uri_sha1=uri_hash)
    if MethodPool.objects.filter(q).exists():
        return True

    w = Q(agent_id__in=[_['id'] for _ in agents]) & Q(uri=api_route.path)
    if IastVulnerabilityModel.objects.filter(w).exists():
        return True
    return False


def checkcover_batch(api_route, agents):
    return api_route.filter(is_cover=1).values(
        "path", "method_id").distinct().count()
    uri_hash = [hashlib.sha1(api_route_.path.encode('utf-8'), usedforsecurity=False).hexdigest()
                for api_route_ in api_route.only('path')]
    cover_count = MethodPool.objects.filter(
        uri_sha1__in=uri_hash,
        agent__in=agents).values('uri_sha1').distinct().count()
    return cover_count


def apiroute_cachekey(api_route, agents, http_method=None):
    agent_id = sha1(str([_['id'] for _ in agents]))
    http_method = str(http_method)
    return "{}_{}_{}".format(agent_id, http_method, api_route.id)


def sha1(string, encoding='utf-8'):
    return hashlib.sha1(string.encode(encoding), usedforsecurity=False).hexdigest()


def get_openapi():
    profilefromdb = IastProfile.objects.filter(key='apiserver').values_list(
        'value', flat=True).first()
    profilefromini = OPENAPI
    profiles = list(
        filter(lambda x: x is not None, [profilefromini, profilefromdb]))
    if profiles == []:
        return None
    return profiles[0]


def validate_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except BaseException:
        return False


logger = logging.getLogger('dongtai-dongtai_conf')


def checkopenapistatus(openapiurl, token):
    try:
        resp = requests.get(
            openapiurl,
            timeout=10,
            headers={'Authorization': "Token {}".format(token)})
        resp = json.loads(resp.content)
        resp = resp.get("data", None)
    except (ConnectionError, ConnectTimeout):
        return False, None
    except Exception as e:
        logger.info("HealthView_{}:{}".format(openapiurl, e))
        return False, None
    return True, resp


METHOD_OVERRIDE_HEADER = 'HTTP_X_HTTP_METHOD_OVERRIDE'


class MethodOverrideMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST' and METHOD_OVERRIDE_HEADER in request.META:
            request.method = request.META[METHOD_OVERRIDE_HEADER]
        return self.get_response(request)


def dict_transfrom(dic: "dict | QuerySet | ValuesQuerySet", key: str):
    return {i[key]: i for i in dic}
