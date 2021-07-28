import json
import logging

from dongtai.endpoint import R, AnonymousAndUserEndPoint
from dongtai.engine.vul_engine import VulEngine
from dongtai.models.agent_method_pool import MethodPool

from iast.serializers.method_pool import MethodPoolListSerialize
from django.db.models import Q
from django.forms.models import model_to_dict
from iast.utils import get_model_field

class MethodPoolSearchProxy(AnonymousAndUserEndPoint):
    def get(self, request):
        page_size = request.GET.get('page_size', 10)
        page = request.GET.get('page', 4)
        fields = ['url', 'res_body']
        fields = get_model_field(
            MethodPool,
            include=[
                'url', 'res_body', 'req_header', 'req_params', 'method_pool'
            ],
        )
        searchfields = dict(
            filter(lambda k: k[0] in fields, request.GET.items()))
        searchfields = {
            ''.join([k, '__iregex']): v
            for k, v in searchfields.items()
        }
        
        q = Q()
        for k, v in searchfields.items():
            params = {k: v}
            q = q | Q(**params)
#        qset = [Q(**{k: v}) for k, v in searchfields.items()]
#        q = set.union(qset)
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
