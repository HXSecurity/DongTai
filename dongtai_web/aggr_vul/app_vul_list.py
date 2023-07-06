from typing import Any
from rest_framework.serializers import ValidationError
from dongtai_common.endpoint import R
from dongtai_common.endpoint import UserEndPoint
from dongtai_common.models.vulnerablity import IastVulnerabilityModel
from dongtai_web.aggregation.aggregation_common import turnIntListOfStr, auth_user_list_str
from dongtai_web.serializers.vul import VulSerializer
from django.utils.translation import gettext_lazy as _
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer
from dongtai_common.models.vulnerablity import IastVulnerabilityStatus
import pymysql
from dongtai_web.serializers.aggregation import AggregationArgsSerializer
from dongtai_common.models import AGGREGATION_ORDER, LANGUAGE_ID_DICT, APP_LEVEL_RISK, APP_VUL_ORDER
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
from dongtai_common.models.dast_integration import IastDastIntegrationRelation
from django.db.models import (Count, Sum)
from itertools import groupby
from collections import defaultdict

INT_LIMIT: int = 2**64 - 1


class GetAppVulsList(UserEndPoint):

    @extend_schema_with_envcheck(
        request=AggregationArgsSerializer,
        tags=[_('app VulList')],
        summary=_('app List Select'),
        description=_("select sca vul and app vul by keywords"),
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
        # user = request.user
        # 获取用户权限
        # auth_user_info = auth_user_list_str(user=user)
        departments = request.user.get_relative_department()
        queryset = IastVulnerabilityModel.objects.filter(
            is_del=0, project_id__gt=0, project__department__in=departments)

        try:
            if ser.is_valid(True):
                page_size = ser.validated_data['page_size']
                page = ser.validated_data['page']
                begin_num = (page - 1) * page_size
                end_num = page * page_size
                # should refact into serilizer
                if begin_num > INT_LIMIT or end_num > INT_LIMIT:
                    return R.failure()
                keywords = ser.validated_data.get("keywords", "")
                es_query = {}
                # 从项目列表进入 绑定项目id
                if ser.validated_data.get("bind_project_id", 0):
                    queryset = queryset.filter(
                        project_id=ser.validated_data.get("bind_project_id"))
                    es_query['bind_project_id'] = ser.validated_data.get(
                        "bind_project_id")
                # 项目版本号
                if ser.validated_data.get("project_version_id", 0):
                    queryset = queryset.filter(
                        project_version_id=ser.validated_data.get(
                            "project_version_id"))
                    es_query['project_version_id'] = ser.validated_data.get(
                        "project_version_id")
                # 按项目筛选
                if ser.validated_data.get("project_id_str", ""):
                    project_id_list = turnIntListOfStr(
                        ser.validated_data.get("project_id_str", ""))
                    queryset = queryset.filter(project_id__in=project_id_list)
                    es_query['project_ids'] = project_id_list
                if ser.validated_data.get("uri", ""):
                    queryset = queryset.filter(
                        uri=ser.validated_data.get("uri", ""))
                # 漏洞类型筛选
                if ser.validated_data.get("hook_type_id_str", ""):
                    vul_type_list = turnIntListOfStr(
                        ser.validated_data.get("hook_type_id_str", ""))
                    queryset = queryset.filter(strategy_id__in=vul_type_list)
                    es_query['strategy_ids'] = vul_type_list
                # 漏洞等级筛选
                if ser.validated_data.get("level_id_str", ""):
                    level_id_list = turnIntListOfStr(
                        ser.validated_data.get("level_id_str", ""))
                    queryset = queryset.filter(level_id__in=level_id_list)
                    es_query['level_ids'] = level_id_list
                # 按状态筛选
                if ser.validated_data.get("status_id_str", ""):
                    status_id_list = turnIntListOfStr(
                        ser.validated_data.get("status_id_str", ""))
                    queryset = queryset.filter(status_id__in=status_id_list)
                    es_query['status_ids'] = status_id_list
                # 按语言筛选
                if ser.validated_data.get("language_str", ""):
                    language_id_list = turnIntListOfStr(
                        ser.validated_data.get("language_str", ""))
                    language_arr = []
                    for lang in language_id_list:
                        language_arr.append(LANGUAGE_ID_DICT.get(str(lang)))
                    queryset = queryset.filter(language__in=language_arr)
                    es_query['language_ids'] = language_arr
                order_list = []
                fields = [
                    "id", "uri", "http_method", "top_stack", "bottom_stack",
                    "level_id", "taint_position", "status_id", "first_time",
                    "latest_time", "strategy__vul_name", "language",
                    "project__name", "server__container", "project_id",
                    'strategy_id', 'project_version_id',
                    'project_version__version_name'
                ]
                if keywords:
                    es_query['search_keyword'] = keywords
                    keywords = pymysql.converters.escape_string(keywords)
                    order_list = ["-score"]
                    fields.append("score")

                    queryset = queryset.annotate(score=SearchLanguageMode(
                        [
                            F('search_keywords'),
                            F('uri'),
                            F('vul_title'),
                            F('http_method'),
                            F('http_protocol'),
                            F('top_stack'),
                            F('bottom_stack')
                        ],
                        search_keyword="+" + keywords,
                    ))
                # 排序
                order_type = APP_VUL_ORDER.get(
                    str(ser.validated_data['order_type']), "level_id")
                order_type_desc = "-" if ser.validated_data[
                    'order_type_desc'] else ""
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
                        departments,
                        page=page,
                        page_size=page_size,
                        **es_query)
                else:
                    vul_data = queryset.values(*tuple(fields)).order_by(
                        *tuple(order_list))[begin_num:end_num]
        except ValidationError as e:
            return R.failure(data=e.detail)
        vul_ids = [vul['id'] for vul in vul_data]
        dastvul_rel_count_res = IastDastIntegrationRelation.objects.filter(
            iastvul_id__in=vul_ids).values('iastvul_id').annotate(
                dastvul_count=Count('dastvul_id'))
        dast_vul_types = IastDastIntegrationRelation.objects.filter(
            iastvul_id__in=vul_ids,
            dastvul__vul_type__isnull=False,
        ).values('dastvul__vul_type', 'iastvul_id').distinct()
        dast_vul_types_dict = defaultdict(
            list, {
                k: list(set(map(lambda x: x['dastvul__vul_type'], g)))
                for k, g in groupby(dast_vul_types,
                                    key=lambda x: x['iastvul_id'])
            })
        dastvul_rel_count_res_dict = defaultdict(
            lambda: 0, {
                item['iastvul_id']: item['dastvul_count']
                for item in dastvul_rel_count_res
            })
        if vul_data:
            for item in vul_data:
                item['level_name'] = APP_LEVEL_RISK.get(
                    str(item['level_id']), "")
                item['server_type'] = VulSerializer.split_container_name(
                    item['server__container'])
                item['is_header_vul'] = VulSerializer.judge_is_header_vul(
                    item['strategy_id'])
                item['agent__project_name'] = item['project__name']
                item['agent__server__container'] = item['server__container']
                item['agent__language'] = item['language']
                item['agent__bind_project_id'] = item['project_id']
                item['header_vul_urls'] = VulSerializer.find_all_urls(
                    item['id']) if item['is_header_vul'] else []
                item['dastvul__vul_type'] = dast_vul_types_dict[item['id']]
                item['dastvul_count'] = dastvul_rel_count_res_dict[item['id']]
                item['dast_validation_status'] = True if dastvul_rel_count_res_dict[
                    item['id']] else False
                end['data'].append(item)
        # all Iast Vulnerability Status
        status = IastVulnerabilityStatus.objects.all()
        status_obj = {}
        for tmp_status in status:
            status_obj[tmp_status.id] = tmp_status.name
        for i in end['data']:
            i['status__name'] = status_obj.get(i['status_id'], "")

        set_vul_inetration(end, request.user.id)
        return R.success(data={
            'messages': end['data'],
            'page': {
                "page_size": page_size,
                "cur_page": page
            }
        }, )

def set_vul_inetration(end: dict[str, Any], user_id: int) -> None:
    pass


def get_vul_list_from_elastic_search(departments,
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
    # user_id_list = [user_id]
    # auth_user_info = auth_user_list_str(user_id=user_id)
    # user_id_list = auth_user_info['user_list']
    from dongtai_common.models.strategy import IastStrategyModel
    from dongtai_common.models.agent import IastAgent
    department_ids = list(departments.values_list("id", flat=True))
    must_query = [
        Q('terms', department_id=department_ids),
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
        department_ids, project_ids, project_version_ids, hook_type_ids, level_ids,
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
                for i in resp]).values('strategy__vul_name', 'language',
                                       'project__name',
                                       'server_id',
                                       'project_id', 'id')
    extra_data_dic = {ex_data['id']: ex_data for ex_data in extra_datas}
    vuls = [i._d_ for i in list(resp)]
    vul_incorrect_id = []
    iast_vulnerability_values = ('language', 'project__name', 'server__container',
                                 'project_id', 'id')
    strategy_values = ('vul_name',)
    for vul in vuls:
        if 'server__container' not in vul:
            vul['server__container'] = ""
        if vul['id'] not in extra_data_dic.keys():
            vul_incorrect_id.append(vul['id'])
            strategy_dic = IastStrategyModel.objects.filter(
                pk=vul['strategy_id']).values(*strategy_values).first()
            iast_vulnerability_dic = IastVulnerabilityModel.objects.filter(pk=vul['agent_id']).values(
                *iast_vulnerability_values).first()
            if not strategy_dic:
                strategy_dic = {i: '' for i in strategy_values}
            if not iast_vulnerability_dic:
                iast_vulnerability_dic = {i: '' for i in iast_vulnerability_values}
            vul['agent__project_name'] = vul['project__name']
            vul['agent__server__container'] = vul['server__container']
            vul['agent__language'] = vul['language']
            vul['agent__bind_project_id'] = vul['project_id']
            for k, v in strategy_dic.items():
                vul['strategy__' + k] = v
            for k, v in iast_vulnerability_dic.items():
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
