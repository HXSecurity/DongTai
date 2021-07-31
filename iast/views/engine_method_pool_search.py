from functools import reduce

from django.db.models import Q
from dongtai.endpoint import R, AnonymousAndUserEndPoint
from dongtai.models.agent import IastAgent
from dongtai.models.agent_method_pool import MethodPool
from dongtai.models.project import IastProject
from dongtai.models.user import User
from dongtai.models.vulnerablity import IastVulnerabilityModel

from iast.utils import get_model_field
import re

class MethodPoolSearchProxy(AnonymousAndUserEndPoint):
    def get(self, request):
        page_size = request.query_params.get('page_size', 1)
        page = request.query_params.get('page_index', 1)
        highlight = request.query_params.get('highlight',1)
        fields = ['url', 'res_body']
        modelfields = [
            'url', 'res_header', 'res_body', 'req_header_fs', 'req_data'
        ]
        fields = get_model_field(
            MethodPool,
            include=modelfields,
        )
        fields.extend(['sinkvalues', 'signature'])
        search_after_keys = ['update_time']
        searchfields = dict(
            filter(lambda k: k[0] in fields, request.query_params.items()))
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
            elif k in fields:
                searchfields_.append((k, v))
        q = reduce(
            lambda x, y: x | y,
            map(
                lambda x: Q(**x),
                map(
                    lambda kv_pair:
                    {'__'.join([kv_pair[0], 'regex']): kv_pair[1]},
                    searchfields_)), Q())
        search_after_fields = dict(
            filter(
                lambda x: x[0] in search_after_keys,
                map(
                    lambda x: (x[0].replace('search_after_', ''),x[1]),
                    filter(lambda x: x[0].startswith('search_after_'),
                           request.query_params.items()))))
        q = reduce(                                                         # fixme to extract out as a function
            lambda x, y: x & y,
            map(
                lambda x: Q(**x),
                map(
                    lambda kv_pair:
                    {'__'.join([kv_pair[0], 'lt']): kv_pair[1]},
                    search_after_fields.items())), q)
        if 'id' in request.query_params.keys():
            q = q & Q(pk=request.query_params['id'])
        queryset = MethodPool.objects.filter(q).order_by('-update_time').all()
        page_size= int(page_size)
        method_pools =  queryset[:page_size]
        method_pools = list(method_pools.values())
        afterkeys = {}
        for i in method_pools[-1:]:
            afterkeys['update_time'] = i['update_time']
        agents = IastAgent.objects.filter(
            pk__in=[i['agent_id'] for i in method_pools]).all().values(
                'bind_project_id', 'token', 'id','user_id')
        projects = IastProject.objects.filter(
            pk__in=[i['bind_project_id']
                    for i in agents]).values('id', 'name', 'user_id')
        vulnerablity = IastVulnerabilityModel.objects.filter(
            method_pool_id__in=[i['id'] for i in method_pools]).all().values(
                'id', 'type', 'method_pool_id', 'level_id').distinct()
        users = User.objects.filter(pk__in=[_['user_id']
                                            for _ in agents]).values(
                                                'id', 'username')
        relations = []
        agents = {_['id']: _ for _ in agents}
        projects = {_['id']: _ for _ in projects}
        vulnerablities = list(vulnerablity)
        users = {_['id']: _ for _ in users}
        for method_pool in method_pools:
            item = {}
            item['method_pool_id'] = method_pool['id']
            agent = agents.get(method_pool['agent_id'], None)
            if agent:
                item['agent_id'] = agent['id']
                item['agent_name'] = agent['token']
                project = projects.get(agent['bind_project_id'], None)
                if project:
                    item['project_id'] = project['id']
                    item['project_name'] = project['name']
                    user = users.get(agent['user_id'], None)
                    if user:
                        item['user_id'] = user['id']
                        item['user_name'] = user['username']
            item['vulnerablities'] = []
            for vulnerablity in list(
                    filter(lambda _: _['method_pool_id'] == method_pool['id'],
                           vulnerablities)):
                _ = {}
                _['vulnerablity_id'] = vulnerablity['id']
                _['vulnerablity_type'] = vulnerablity['type']
                _['level_id'] = vulnerablity['level_id']
                item['vulnerablities'].append(_)
            relations.append(item)
        aggregation = {}
        aggregation['vulnerablities_count'] = list(
            map(
                lambda x: {
                    'method_pool_id': x['method_pool_id'],
                    'count': len(x['vulnerablities'])
                }, relations))
        if highlight:
            for method_pool in method_pools:
                for field in modelfields:
                    if field in searchfields.keys() and request.GET.get(
                            field, None):
                        method_pool['_'.join([field, 'highlight'
                                              ])] = highlight_matches(
                                                  request.GET[field],
                                                  method_pool[field],
                                                  "<em>{0}</em>")
        return R.success(
            data={
                'method_pools': method_pools,
                'relations': relations,
                'aggregation': aggregation,
                'afterkeys': afterkeys
            })


def highlight_matches(query, text, html):
    text = text.replace('<', '&lt;')
    def span_matches(match):
        return html.format(match.group(0))
    return re.sub(query, span_matches, text, flags=re.I)
