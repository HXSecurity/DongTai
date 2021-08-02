from functools import reduce

from django.db.models import Q
from dongtai.endpoint import R, AnonymousAuthEndPoint
from dongtai.models.agent import IastAgent
from dongtai.models.agent_method_pool import MethodPool
from dongtai.models.project import IastProject
from dongtai.models.user import User
from dongtai.models.vulnerablity import IastVulnerabilityModel

from iast.utils import get_model_field, assemble_query
import re
import operator
class MethodPoolSearchProxy(AnonymousAuthEndPoint):
    def get(self, request):
        page_size = int(request.query_params.get('page_size', 1))
        page = request.query_params.get('page_index', 1)
        highlight = request.query_params.get('highlight',1)
        fields = ['url', 'res_body']
        model_fields = [
            'url', 'res_header', 'res_body', 'req_header_fs', 'req_data'
        ]
        fields = get_model_field(
            MethodPool,
            include=model_fields,
        )
        fields.extend(['sinkvalues', 'signature'])
        search_after_keys = ['update_time']
        search_fields = dict(
            filter(lambda k: k[0] in fields, request.query_params.items()))
        search_fields_ = []
        for k, v in search_fields.items():
            if k == 'sinkvalues':  # 污点数据
                templates = [
                    r'"targetValues": ".*{}.*"', r'"sourceValues": ".*{}.*"'
                ]
                search_fields_.extend(
                    map(lambda x: ('method_pool', x.format(v)), templates))
            elif k == 'signature':  # 方法签名
                templates = [r'"signature": ".*{}.*"']
                search_fields_.extend(
                    map(lambda x: ('method_pool', x.format(v)), templates))
            elif k in fields:
                search_fields_.append((k, v))
        q = assemble_query(search_fields_, 'regex', Q(), operator.or_)
        search_after_fields = list(
            filter(
                lambda x: x[0] in search_after_keys,
                map(
                    lambda x: (x[0].replace('search_after_', ''), x[1]),
                    filter(lambda x: x[0].startswith('search_after_'),
                           request.query_params.items()))))
        q = assemble_query(search_after_fields, 'lt', q, operator.and_)
        if 'id' in request.query_params.keys():
            q = assemble_query(search_after_fields, '', q, operator.and_)
        q = q & Q(agent_id__in=[item['id'] for item in list(self.get_auth_agents_with_user(request.user).values('id'))])
        queryset = MethodPool.objects.filter(q).order_by('-update_time')[:page_size]
        method_pools = list(queryset.values())
        afterkeys = {}
        for i in method_pools[-1:]:
            afterkeys['update_time'] = i['update_time']
        agents = IastAgent.objects.filter(
            pk__in=[i['agent_id'] for i in method_pools]).all().values(
                'bind_project_id', 'token', 'id', 'user_id', 'is_running')
        projects = IastProject.objects.filter(
            pk__in=[i['bind_project_id']
                    for i in agents]).values('id', 'name', 'user_id')
        vulnerablity = IastVulnerabilityModel.objects.filter(
            method_pool_id__in=[i['id'] for i in method_pools]).all().values(
                'id', 'type', 'method_pool_id', 'level_id').distinct()
        users = User.objects.filter(pk__in=[_['user_id']
                                            for _ in agents]).values(
                                                'id', 'username')
        vulnerablities = list(vulnerablity)
        relations = []
        [agents, projects, users] = _transform([agents, projects, users], 'id')
        for method_pool in method_pools:
            item = {}
            item['method_pool_id'] = method_pool['id']
            agent = agents.get(method_pool['agent_id'], None)
            if agent:
                item['agent_id'] = agent['id']
                item['agent_name'] = agent['token']
                item['agent_is_running'] = agent['is_running']
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
        aggregation['vulnerablities_count'] = aggregation_count(
            relations, 'method_pool_id', 'vulnerablities')
        if highlight:
            for method_pool in method_pools:
                for field in model_fields:
                    if field in search_fields.keys() and request.GET.get(
                            field, None):
                        if method_pool[field] is None:
                            continue
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


def _transform(models: list, reindex_id: str):
    return [{_[reindex_id]: _ for _ in model} for model in models]


def aggregation_count(list_, primary_key, count_key):
    """
    params   
    list_ : [{},{}]
    """
    return list(
        map(
            lambda x: {
                primary_key: x[primary_key],
                'count': len(x[count_key])
            }, list_))



def highlight_matches(query, text, html):
    text = text.replace('<', '&lt;')
    def span_matches(match):
        return html.format(match.group(0))
    return re.sub(query, span_matches, text, flags=re.I)
