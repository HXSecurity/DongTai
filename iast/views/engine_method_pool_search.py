import json
import logging

from dongtai.endpoint import R, AnonymousAndUserEndPoint
from dongtai.engine.vul_engine import VulEngine
from dongtai.models.agent_method_pool import MethodPool

from iast.serializers.method_pool import MethodPoolListSerialize
from django.db.models import Q
from django.forms.models import model_to_dict
from iast.utils import get_model_field
from functools import reduce
class MethodPoolSearchProxy(AnonymousAndUserEndPoint):
    def get(self, request):
        page_size = request.GET.get('page_size', 10)
        page = request.GET.get('page_index', 1)
        fields = ['url', 'res_body']
        fields = get_model_field(
            MethodPool,
            include=[
                'url', 'res_body', 'req_header', 'req_data'
            ],
        )
        fields.extend(['sinkvalues', 'signature'])
        searchfields = dict(
            filter(lambda k: k[0] in fields, request.GET.items()))
        searchfields_ = []
        for k, v in searchfields.items():
            if k == 'sinks':  # 污点数据
                templates = [
                    r'"targetValues": ".*{}.*"', r'"sourceValues": ".*{}.*"'
                ]
                searchfields_.extend(
                    map(lambda x: ('method_pool', x.format(v), templates)))
            elif k == 'signature':  # 方法签名
                templates = [r'"signature": ".*{}.*"']
                searchfields_.extend(
                    map(lambda x: ('method_pool', x.format(v), templates)))
            else:
                searchfields_.append((k, v))
        q = reduce(
            lambda x, y: x | y,
            map(
                lambda x: Q(**x),
                map(
                    lambda kv_pair:
                    {'__'.join([kv_pair[0], 'regex']): kv_pair[1]},
                    searchfields_)), Q())
        queryset = MethodPool.objects.filter(q).order_by('-create_time').all()
        page_summary, method_pools = self.get_paginator(
            queryset, page, page_size)
        return R.success(
            data={
                'method_pools':
                [model_to_dict(method_pool) for method_pool in method_pools],
                'summary':
                page_summary
            })
