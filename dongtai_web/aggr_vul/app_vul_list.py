from rest_framework.serializers import ValidationError
from dongtai_common.endpoint import R
from dongtai_common.endpoint import UserEndPoint
from dongtai_common.models.vulnerablity import IastVulnerabilityModel
from dongtai_web.aggregation.aggregation_common import turnIntListOfStr,auth_user_list_str
from dongtai_web.serializers.vul import VulSerializer
from django.utils.translation import gettext_lazy as _
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer
from dongtai_common.models.vulnerablity import IastVulnerabilityStatus
import pymysql
from dongtai_web.serializers.aggregation import AggregationArgsSerializer
from dongtai_common.models import AGGREGATION_ORDER,LANGUAGE_ID_DICT,APP_LEVEL_RISK,APP_VUL_ORDER
from django.db.models import F
from dongtai_common.utils.db import SearchLanguageMode
from dongtai_common.models.vulnerablity import IastVulnerabilityDocument
from elasticsearch_dsl import Q, Search
from elasticsearch import Elasticsearch
from elasticsearch_dsl import A
from dongtai_common.models.strategy import IastStrategyModel
from dongtai_common.models.vulnerablity import IastVulnerabilityStatus
from dongtai_common.models.program_language import IastProgramLanguage
from dongtai_common.models.project import IastProject
from dongtai_common.models.vul_level import IastVulLevel
from django.core.cache import cache
from dongtai_conf import settings
from dongtai_common.common.utils import make_hash
from dongtai_conf.settings import ELASTICSEARCH_STATE
from dongtai_engine.elatic_search.data_correction import data_correction_interpetor

class GetAppVulsList(UserEndPoint):

    @ extend_schema_with_envcheck(
        request=AggregationArgsSerializer,
        tags=[_('app VulList')],
        summary=_('app List Select'),
        description=_(
            "select sca vul and app vul by keywords"
        ),
    )
    def post(self, request):
        """
        :param request:
        :return:
        """
        end = {
            "status": 201,
            "msg": "success",
            "data": [],
        }
        ser = AggregationArgsSerializer(data=request.data)
        user = request.user
        # 获取用户权限
        auth_user_info = auth_user_list_str(user=user)
        queryset = IastVulnerabilityModel.objects.filter(is_del=0,agent__bind_project_id__gt=0,agent__user_id__in=auth_user_info['user_list'])

        try:
            if ser.is_valid(True):
                page_size = ser.validated_data['page_size']
                page = ser.validated_data['page']
                begin_num = (page - 1) * page_size
                end_num = page * page_size
                keywords = ser.validated_data.get("keywords", "")
                es_query = {}
                # 从项目列表进入 绑定项目id
                if ser.validated_data.get("bind_project_id", 0):
                    queryset = queryset.filter(agent__bind_project_id=ser.validated_data.get("bind_project_id"))
                    es_query['bind_project_id'] = ser.validated_data.get("bind_project_id")
                # 项目版本号
                if ser.validated_data.get("project_version_id", 0):
                    queryset = queryset.filter(agent__project_version_id=ser.validated_data.get("project_version_id"))
                    es_query['project_version_id'] = ser.validated_data.get("project_version_id")
                # 按项目筛选
                if ser.validated_data.get("project_id_str", ""):
                    project_id_list = turnIntListOfStr(ser.validated_data.get("project_id_str", ""))
                    queryset = queryset.filter(agent__bind_project_id__in=project_id_list)
                    es_query['project_ids'] = project_id_list
                # 漏洞类型筛选
                if ser.validated_data.get("hook_type_id_str", ""):
                    vul_type_list = turnIntListOfStr(ser.validated_data.get("hook_type_id_str", ""))
                    queryset = queryset.filter(strategy_id__in=vul_type_list)
                    es_query['strategy_ids'] = vul_type_list
                # 漏洞等级筛选
                if ser.validated_data.get("level_id_str", ""):
                    level_id_list = turnIntListOfStr(ser.validated_data.get("level_id_str", ""))
                    queryset = queryset.filter(level_id__in=level_id_list)
                    es_query['level_ids'] = level_id_list
                # 按状态筛选
                if ser.validated_data.get("status_id_str", ""):
                    status_id_list = turnIntListOfStr(ser.validated_data.get("status_id_str", ""))
                    queryset = queryset.filter(status_id__in=status_id_list)
                    es_query['status_ids'] = status_id_list
                # 按语言筛选
                if ser.validated_data.get("language_str", ""):
                    language_id_list = turnIntListOfStr(ser.validated_data.get("language_str", ""))
                    language_arr = []
                    for lang in language_id_list:
                        language_arr.append(LANGUAGE_ID_DICT.get(str(lang)))
                    queryset = queryset.filter(agent__language__in=language_arr)
                    es_query['language_ids'] = language_arr
                order_list = []
                fields = ["id", "uri","http_method","top_stack","bottom_stack","level_id",
                            "taint_position","status_id","first_time","latest_time", "strategy__vul_name","agent__language",
                            "agent__project_name","agent__server__container","agent__bind_project_id"
                            ]
                if keywords:
                    es_query['search_keyword'] = keywords
                    keywords = pymysql.converters.escape_string(keywords)
                    order_list = ["-score"]
                    fields.append("score")

                    queryset = queryset.annotate(score=SearchLanguageMode([F('search_keywords'), F('uri'), F('vul_title'), F('http_method'), F('http_protocol'), F('top_stack'), F('bottom_stack')], search_keyword=keywords))
                # 排序
                order_type = APP_VUL_ORDER.get(str(ser.validated_data['order_type']), "level_id")
                order_type_desc = "-" if ser.validated_data['order_type_desc'] else ""
                if order_type == "level_id":
                    order_list.append(order_type_desc + order_type)
                    if ser.validated_data['order_type_desc']:
                        order_list.append("-latest_time")
                    else:
                        order_list.append("latest_time_desc")
                else:
                    order_list.append(order_type_desc + order_type)
                es_query['order'] = order_type_desc + order_type
                if ELASTICSEARCH_STATE:
                    vul_data = get_vul_list_from_elastic_search(
                        request.user.id,
                        page=page,
                        page_size=page_size,
                        **es_query)
                else:
                    vul_data = queryset.values(*tuple(fields)).order_by(*tuple(order_list))[begin_num:end_num]
        except ValidationError as e:
            return R.failure(data=e.detail)

        if vul_data:
            for item in vul_data:
                item['level_name'] = APP_LEVEL_RISK.get(str(item['level_id']),"")
                item['server_type'] = VulSerializer.split_container_name(item['agent__server__container'])
                end['data'].append(item)

        # all Iast Vulnerability Status
        status = IastVulnerabilityStatus.objects.all()
        status_obj = {}
        for tmp_status in status:
            status_obj[tmp_status.id] = tmp_status.name
        for i in end['data']:
            i['status__name'] = status_obj.get(i['status_id'], "")


        return R.success(data={
            'messages': end['data'],
            'page': {
                "page_size": page_size,
                "cur_page": page
            }
        }, )


def get_vul_list_from_elastic_search(user_id,
                                     project_ids=[],
                                     project_version_ids=[],
                                     hook_type_ids=[],
                                     level_ids=[],
                                     status_ids=[],
                                     strategy_ids=[],
                                     language_ids=[],
                                     search_keyword="",
                                     page=1,
                                     page_size=10,
                                     bind_project_id=0,
                                     project_version_id=0,
                                     order=""):
    user_id_list = [user_id]
    auth_user_info = auth_user_list_str(user_id=user_id)
    user_id_list = auth_user_info['user_list']
    from dongtai_common.models.strategy import IastStrategyModel
    from dongtai_common.models.agent import IastAgent
    must_query = [
        Q('terms', user_id=user_id_list),
        Q('terms', is_del=[0]),
        Q('range', bind_project_id={'gt': 0}),
        Q('range', strategy_id={'gt': 0}),
    ]
    order_list = ['_score', 'level_id', '-latest_time', '-id']
    if order:
        order_list.insert(0, order)
    if bind_project_id:
        must_query.append(Q('terms', bind_project_id=[bind_project_id]))
    if project_version_id:
        must_query.append(Q('terms', project_version_id=[project_version_id]))
    if project_ids:
        must_query.append(Q('terms', project_id=project_ids))
    if project_version_ids:
        must_query.append(Q('terms', project_version_id=project_version_ids))
    if level_ids:
        must_query.append(Q('terms', level_id=level_ids))
    if status_ids:
        must_query.append(Q('terms', status_id=status_ids))
    if language_ids:
        must_query.append(Q('terms', **{"language.keyword": language_ids}))
    if strategy_ids:
        must_query.append(Q('terms', strategy_id=strategy_ids))
    if search_keyword:
        must_query.append(
            Q('multi_match',
              query=search_keyword,
              fields=[
                  "search_keywords", "uri", "vul_title", "http_protocol",
                  "top_stack", "bottom_stack"
              ]))
    a = Q('bool',
          must=must_query)
    hashkey = make_hash([
        user_id, project_ids, project_version_ids, hook_type_ids, level_ids,
        status_ids, language_ids, search_keyword, page_size, bind_project_id,
        project_version_id
    ])
    if page == 1:
        cache.delete(hashkey)
    after_table = cache.get(hashkey, {})
    after_key = after_table.get(page, None)
    extra_dict = {}
    if after_key:
        extra_dict['search_after'] = after_key
    res = IastVulnerabilityDocument.search().query(a).extra(**extra_dict).sort(
        *order_list)[:page_size].using(
            Elasticsearch(settings.ELASTICSEARCH_DSL['default']['hosts']))
    resp = res.execute()
    extra_datas = IastVulnerabilityModel.objects.filter(
        pk__in=[i['id']
                for i in resp]).values('strategy__vul_name', 'agent__language',
                                       'agent__project_name',
                                       'agent__server__container',
                                       'agent__bind_project_id', 'id')
    extra_data_dic = {ex_data['id']: ex_data for ex_data in extra_datas}
    vuls = [i._d_ for i in list(resp)]
    vul_incorrect_id = []
    agent_values = ('language', 'project_name', 'server__container',
                    'bind_project_id', 'id')
    strategy_values = ('vul_name', )
    for vul in vuls:
        if vul['id'] not in extra_data_dic.keys():
            vul_incorrect_id.append(vul['id'])
            strategy_dic = IastStrategyModel.objects.filter(
                pk=vul['strategy_id']).values(*strategy_values).first()
            agent_dic = IastAgent.objects.filter(pk=vul['agent_id']).values(
                *agent_values).first()
            if not strategy_dic:
                strategy_dic = {i: '' for i in strategy_values}
            if not agent_dic:
                agent_dic = {i: '' for i in agent_values}
            for k, v in strategy_dic.items():
                vul['strategy__' + k] = v
            for k, v in agent_dic.items():
                vul['agent__' + k] = v
        else:
            vul.update(extra_data_dic[vul['id']])
    if vul_incorrect_id:
        data_correction_interpetor.delay('vulnerablity_sync_fail')
    if resp.hits:
        afterkey = resp.hits[-1].meta['sort']
        after_table[page + 1] = afterkey
        cache.set(hashkey, after_table)
    return vuls
