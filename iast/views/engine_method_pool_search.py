from functools import reduce

from django.db.models import Q
from dongtai.endpoint import R, AnonymousAndUserEndPoint
from dongtai.models.agent import IastAgent
from dongtai.models.agent_method_pool import MethodPool
from dongtai.models.project import IastProject
from dongtai.models.user import User
from dongtai.models.vulnerablity import IastVulnerabilityModel
from dongtai.models.hook_type import HookType
from dongtai.models.strategy import IastStrategyModel

from iast.utils import get_model_field, assemble_query,assemble_query_2
from iast.utils import extend_schema_with_envcheck, get_response_serializer
from django.utils.translation import gettext_lazy
from django.db.utils import OperationalError
import re
import operator
import time
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext_lazy


class MethodPoolSearchProxySer(serializers.Serializer):
    page_size = serializers.IntegerField(min_value=1,
                                         help_text=_("number per page"))
    highlight = serializers.IntegerField(
        default=1,
        help_text=
        _("Whether to enable highlighting, the text where the regular expression matches will be highlighted"
          ))
    exclude_ids = serializers.ListField(
        child=serializers.IntegerField(),
        help_text=
        _("Exclude the method_pool entry with the following id, this field is used to obtain the data of the entire project in batches."
          ),
        required=False)
    time_range = serializers.ListField(
        child=serializers.IntegerField(
            min_value=1, help_text=_('time  format such as 1,1628190947242')),
        min_length=2,
        max_length=2,
        help_text=
        _("Time range, the default is the current time to the previous seven days, separated by',', format such as 1,1628190947242"
          ))
    url = serializers.CharField(
        help_text=_("The url of the method pool, search using regular syntax"),
        required=False)
    res_header = serializers.CharField(help_text=_(
        "The response header of the method pood, search using regular syntax"),
                                       required=False)
    res_body = serializers.CharField(help_text=_(
        "The response body of the calling chain, search using regular syntax"),
                                     required=False)
    req_header_fs = serializers.CharField(help_text=_(
        "The request header of the calling chain, search using regular syntax"
    ),
                                          required=False)
    req_data = serializers.CharField(help_text=_(
        "The request data of the calling chain, search using regular syntax"),
                                     required=False)
    sinkvalues = serializers.CharField(help_text=_(
        "The sinkvalues of the calling chain, search using regular syntax"),
                                       required=False)
    signature = serializers.CharField(help_text=_(
        "The signature of the calling chain, search using regular syntax"),
                                      required=False)
    update_time = serializers.CharField(help_text=_(
        "The filter field will return the method call chain with the update time after this time, which can be combined with the exclude_ids field to handle paging"
    ),
                                        required=False)
    search_mode = serializers.IntegerField(
        help_text=_("the search_mode , 1-regex match ,2-regex not match "),
        default=1,
        required=False)


class MethodPoolSearchResponseRelationVulnerablitySer(serializers.Serializer):
    vulnerablity_type = serializers.CharField()
    vulnerablity_hook_type_id = serializers.IntegerField()
    vulnerablity_id = serializers.IntegerField()
    level_id = serializers.IntegerField()


class MethodPoolSearchResponseMethodPoolSer(serializers.Serializer):
    id = serializers.IntegerField()
    agent_id = serializers.IntegerField()
    url = serializers.CharField()
    uri = serializers.CharField()
    http_method = serializers.CharField()
    http_scheme = serializers.CharField()
    http_protocol = serializers.CharField()
    req_header = serializers.CharField()
    req_header_fs = serializers.CharField()
    req_params = serializers.CharField()
    req_data = serializers.CharField()
    res_header = serializers.CharField()
    res_body = serializers.CharField()
    context_path = serializers.CharField()
    method_pool = serializers.CharField()
    pool_sign = serializers.CharField()
    client_ip = serializers.CharField()
    update_time = serializers.IntegerField()
    create_time = serializers.IntegerField()
    uri_sha1 = serializers.CharField()
    uri_highlight = serializers.CharField()
    res_header_highlight = serializers.CharField()
    res_body_highlight = serializers.CharField()
    req_header_fs_highlight = serializers.CharField()
    req_data_highlight = serializers.CharField()


class MethodPoolSearchResponseRelationSer(serializers.Serializer):
    method_pool_id = serializers.IntegerField()
    agent_id = serializers.IntegerField()
    agent_name = serializers.CharField()
    agent_is_running = serializers.IntegerField()
    project_name = serializers.CharField()
    user_id = serializers.IntegerField()
    user_name = serializers.CharField()
    vulnerablities = MethodPoolSearchResponseRelationVulnerablitySer(many=True)


class MethodPoolSearchResponseAggregationSer(serializers.Serializer):
    method_pool_id = serializers.IntegerField()
    count = serializers.IntegerField()


class MethodPoolSearchResponseAfterkeySer(serializers.Serializer):
    update_time = serializers.IntegerField()


class MethodPoolSearchResponseSer(serializers.Serializer):
    method_pools = MethodPoolSearchResponseMethodPoolSer(many=True)
    relations = MethodPoolSearchResponseRelationSer(many=True)
    aggregation = MethodPoolSearchResponseAggregationSer(many=True)
    afterkeys = MethodPoolSearchResponseAfterkeySer(many=True)


_GetResponseSerializer = get_response_serializer(MethodPoolSearchResponseSer())


class MethodPoolSearchProxy(AnonymousAndUserEndPoint):
    @extend_schema_with_envcheck(
        request=MethodPoolSearchProxySer,
        tags=[_('Method Pool')],
        summary=_('Method Pool Search'),
        description=
        _("Search for the method pool information according to the following conditions, the default is regular expression input, regular specifications refer to REGEX POSIX 1003.2"
          ),
        response_schema=_GetResponseSerializer,
    )
    def post(self, request):
        page_size = int(request.data.get('page_size', 1))
        page = request.data.get('page_index', 1)
        highlight = request.data.get('highlight', 1)
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
        exclude_ids = request.data.get('exclude_ids', None)
        time_range = request.data.get('time_range', None) 
        try:
            search_mode = int(request.data.get('search_mode', 1))
            if page_size <= 0:
                return R.failure(gettext_lazy("Parameter error"))
            [start_time,
             end_time] = time_range if time_range is not None and len(
                 time_range) == 2 and 0 < time_range[1] - time_range[
                     0] <= 60 * 60 * 24 * 7 else [
                         int(time.time()) - 60 * 60 * 24 * 7,
                         int(time.time())
                     ]
            ids = exclude_ids if isinstance(exclude_ids, list) and all(
                map(lambda x: isinstance(x, int), exclude_ids)) else []
        except:
            return R.failure(gettext_lazy("Parameter error"))
        search_fields = dict(
            filter(lambda k: k[0] in fields, request.data.items()))
        search_fields_ = []
        for k, v in search_fields.items():
            if k == 'sinkvalues':
                templates = [
                    r'"targetValues": ".*{}.*"', r'"sourceValues": ".*{}.*"'
                ]
                search_fields_.extend(
                    map(lambda x: ('method_pool', x.format(v)), templates))
            elif k == 'signature':
                templates = [r'"signature": ".*{}.*"']
                search_fields_.extend(
                    map(lambda x: ('method_pool', x.format(v)), templates))
            elif k in fields:
                search_fields_.append((k, v))
        if search_mode == 1:
            q = assemble_query(search_fields_, 'regex', Q(), operator.or_)
        elif search_mode == 2:
            q = assemble_query_2(search_fields_, 'regex', Q(), operator.and_)
        search_after_fields = list(
            filter(
                lambda x: x[0] in search_after_keys,
                map(
                    lambda x: (x[0].replace('search_after_', ''), x[1]),
                    filter(lambda x: x[0].startswith('search_after_'),
                           request.data.items()))))
        q = q if 'q' in vars() else Q()
        q = assemble_query(search_after_fields, 'lte', q, operator.and_)  
        if 'id' in request.data.keys():
            q = q & Q(pk=request.data['id'])
        q = q & Q(agent_id__in=[
            item['id'] for item in list(
                self.get_auth_agents_with_user(request.user).values('id'))
        ])
        q = (q &
             (Q(update_time__gte=start_time) & Q(update_time__lte=end_time)))
        q = (q & (~Q(pk__in=ids))) if ids is not None and ids != [] else q
        queryset = MethodPool.objects.filter(q).order_by(
            '-update_time')[:page_size]
        try:
            method_pools = list(queryset.values())
        except OperationalError as e:
            return R.failure(msg=gettext_lazy("The regular expression format is wrong, please use REGEX POSIX 1003.2"))
        afterkeys = {}
        for i in method_pools[-1:]:
            afterkeys['update_time'] = i['update_time']
        agents = IastAgent.objects.filter(
            pk__in=[i['agent_id'] for i in method_pools]).all().values(
                'bind_project_id', 'token', 'id', 'user_id', 'online')
        projects = IastProject.objects.filter(
            pk__in=[i['bind_project_id']
                    for i in agents]).values('id', 'name', 'user_id')
        vulnerablity = IastVulnerabilityModel.objects.filter(
            method_pool_id__in=[i['id'] for i in method_pools]).all().values(
                'id', 'hook_type_id','hook_type__name', 'strategy__vul_name','strategy_id','method_pool_id', 'level_id').distinct()
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
                item['agent_is_running'] = agent['online']
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
                type_ = list(
                    filter(lambda x: x is not None, [vulnerablity['strategy__vul_name'], vulnerablity['hook_type__name']]))
                _['vulnerablity_type'] = type_[0] if type_ else ''
                _['vulnerablity_id'] = vulnerablity['id']
                _['vulnerablity_hook_type_id'] = vulnerablity['hook_type_id']
                _['level_id'] = vulnerablity['level_id']
                item['vulnerablities'].append(_)
            relations.append(item)
        aggregation = {}
        aggregation['vulnerablities_count'] = aggregation_count(
            relations, 'method_pool_id', 'vulnerablities')
        if highlight:
            for method_pool in method_pools:
                for field in model_fields:
                    if field in search_fields.keys() and request.data.get(
                            field, None) and search_mode == 1:
                        if method_pool[field] is None:
                            continue
                        method_pool['_'.join([field, 'highlight'
                                              ])] = highlight_matches(
                                                  request.data[field],
                                                  method_pool[field],
                                                  "<em>{0}</em>")
                    elif field in fields:
                        if method_pool[field] is None:
                            continue
                        method_pool['_'.join([field, 'highlight'
                                              ])] = method_pool[field].replace(
                                                  '<', '&lt;')
                    else:
                        if method_pool[field] is None:
                            continue
                        method_pool['_'.join([field, 'highlight'
                                              ])] = method_pool[field].replace(
                                                  '<', '&lt;')
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
