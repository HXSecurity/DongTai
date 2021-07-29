from functools import reduce

from django.db.models import Q
from dongtai.endpoint import R, AnonymousAndUserEndPoint
from dongtai.models.agent import IastAgent
from dongtai.models.agent_method_pool import MethodPool
from dongtai.models.project import IastProject
from dongtai.models.user import User
from dongtai.models.vulnerablity import IastVulnerabilityModel

from iast.utils import get_model_field


class MethodPoolSearchProxy(AnonymousAndUserEndPoint):
    def get(self, request):
        page_size = request.query_params.get('page_size', 10)
        page = request.query_params.get('page_index', 1)
        fields = ['url', 'res_body']
        fields = get_model_field(
            MethodPool,
            include=[
                'url', 'res_header', 'res_body', 'req_header_fs', 'req_data'
            ],
        )
        fields.extend(['sinkvalues', 'signature'])
        searchfields = dict(
            filter(lambda k: k[0] in fields, request.GET.items()))
        searchfields_ = []
        for k, v in searchfields.items():
            if k == 'sinkvalues':  # 污点数据
                templates = [
                    r'"targetValues": ".*{}.*"', r'"sourceValues": ".*{}.*"'
                ]
                searchfields_.extend(
                    map(lambda x: ('method_pool', x.format(v)), templates))
            elif k == 'signature':  # 方法签名
                templates = [r'"signature": ".*{}.*"']
                searchfields_.extend(
                    map(lambda x: ('method_pool', x.format(v)), templates))
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
        method_pools = list(method_pools.values())
        agents = IastAgent.objects.filter(
            pk__in=[i['agent_id'] for i in method_pools]).all().values(
                'bind_project_id', 'token', 'id')
        projects = IastProject.objects.filter(
            pk__in=[i['bind_project_id']
                    for i in agents]).values('id', 'name', 'user_id')
        vulnerablity = IastVulnerabilityModel.objects.filter(
            method_pool_id__in=[i['id'] for i in method_pools]).all().values(
                'id', 'type', 'method_pool_id').distinct()
        users = User.objects.filter(pk__in=[_['user_id']
                                            for _ in projects]).values(
                                                'id', 'username')
        relations = []
        agents = {_['id']: _ for _ in agents}
        projects = {_['id']: _ for _ in projects}
        vulnerablities = list(vulnerablity)
        users = {_['id']: _ for _ in users}
        for method_pool in method_pools:
            item = {}
            item['method_pool.id'] = method_pool['id']
            agent = agents.get(method_pool['agent_id'], None)
            if agent:
                item['agent.id'] = agent['id']
                item['agent.name'] = agent['token']
                project = projects.get('bind_project_id', None)
                if project:
                    item['project.id'] = project['id']
                    item['project.name'] = project['name']
                    user = users.get(project['user_id'])
                    if user:
                        item['user.id'] = user['id']
                        item['user.name'] = user['name']
            item['vulnerablities'] = []
            for vulnerablity in list(
                    filter(lambda _: _['method_pool_id'] == method_pool['id'],
                           vulnerablities)):
                _ = {}
                _['vulnerablity.id'] = vulnerablity['id']
                _['vulnerablity.type'] = vulnerablity['type']
                item['vulnerablities'].append(_)
            relations.append(item)
        aggregation = {}
        aggregation['vulnerablities_count'] = list(
            map(
                lambda x: {
                    'method_pools.id': x['method_pool.id'],
                    'count': len(x['vulnerablities'])
                }, relations))
        return R.success(
            data={
                'method_pools': method_pools,
                'relations': relations,
                'summary': page_summary,
                'aggregation': aggregation
            })
