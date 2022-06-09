import copy

from dongtai_common.endpoint import UserEndPoint
from dongtai_web.utils import extend_schema_with_envcheck
from dongtai_web.serializers.aggregation import AggregationArgsSerializer
from django.utils.translation import gettext_lazy as _
from dongtai_common.endpoint import R
from dongtai_web.aggregation.aggregation_common import auth_user_list_str
from dongtai_common.models import LANGUAGE_DICT
from rest_framework.serializers import ValidationError
from django.db import connection
from dongtai_common.common.utils import cached_decorator
from dongtai_common.models import APP_LEVEL_RISK

def get_annotate_sca_common_data(user_id: int, pro_condition: str):
    return get_annotate_sca_base_data(user_id,pro_condition)

@cached_decorator(random_range=(2 * 60 * 60, 2 * 60 * 60), use_celery_update=True)
def get_annotate_sca_cache_data(user_id: int,pro_condition: str):
    return get_annotate_sca_base_data(user_id,pro_condition)

def get_annotate_sca_base_data(user_id: int,pro_condition: str):
    base_summary = {
        "level": [],
        "availability": {
            "have_poc": {
                "name": "存在利用代码",
                "num": 0,
                "id": 1
            },
            "have_article": {
                "name": "存在分析文章",
                "num": 0,
                "id": 2
            },
            "no_availability": {
                "name": "无利用信息",
                "num": 0,
                "id": 3
            },
        },
        "hook_type": [],
        "language": [],
        "project": []
    }
    # auth_condition = getAuthBaseQuery(user_id=user_id, table_str="asset")
    user_auth_info = auth_user_list_str(user_id=user_id,user_table="asset")
    query_condition = " where rel.is_del=0 and asset.project_id>0 " + user_auth_info.get("user_condition_str") + pro_condition
    base_join = "left JOIN iast_asset_vul_relation as rel on rel.asset_vul_id=vul.id  " \
                "left JOIN iast_asset as asset on rel.asset_id=asset.id "
    # level_join = "left JOIN iast_vul_level as level on level.id=vul.level_id "


    with connection.cursor() as cursor:
        count_level_query = "SELECT  vul.level_id,count( DISTINCT(vul.id ))  from iast_asset_vul as vul  " \
                            + base_join + query_condition + " group by vul.level_id  "
        result_summary = base_summary

        # level_summary = IastVulLevel.objects.raw(count_level_query)
        cursor.execute(count_level_query)
        level_summary = cursor.fetchall()
        if level_summary:
            for item in level_summary:
                level_id , count = item
                result_summary['level'].append({
                    "name": APP_LEVEL_RISK.get(str(level_id), "None"),
                    "num": count,
                    "id": level_id
                })

        # 存在利用代码
        count_poc_query = "SELECT count(DISTINCT( vul.id )) as have_poc_count from iast_asset_vul as vul  " \
                          + base_join + query_condition + " and  vul.have_poc=1 "
        cursor.execute(count_poc_query)
        poc_summary = cursor.fetchone()
        if poc_summary:
            result_summary['availability']['have_poc']['num'] = poc_summary[0]
        # 存在分析文章
        count_article_query = "SELECT count(DISTINCT( vul.id )) as have_article_count from iast_asset_vul as vul  " \
                              + base_join + query_condition + " and  vul.have_article=1 "
        cursor.execute(count_article_query)
        article_summary = cursor.fetchone()
        if article_summary:
            result_summary['availability']['have_article']['num'] = article_summary[0]
        # 无利用信息
        count_no_availability_query = "SELECT count(DISTINCT( vul.id )) as no_availability from iast_asset_vul as vul  " \
                                      + base_join + query_condition + " and  vul.have_article=0 and  vul.have_poc=0 "
        cursor.execute(count_no_availability_query)
        no_availability_summary = cursor.fetchone()
        if no_availability_summary:
            result_summary['availability']['no_availability']['num'] = no_availability_summary[0]

        count_language_query = "SELECT  vul.package_language, count( DISTINCT(vul.id )) AS count_package_language  from iast_asset_vul as vul  " \
                               + base_join + query_condition + " group by vul.package_language  "
        cursor.execute(count_language_query)
        language_summary = cursor.fetchall()
        lang_arr = copy.copy(LANGUAGE_DICT)
        lang_key = lang_arr.keys()
        if language_summary:
            for item in language_summary:
                package_language,count_package_language = item
                result_summary['language'].append({
                    "id": lang_arr.get(str(package_language)),
                    "num": count_package_language,
                    "name": package_language
                })
                if package_language in lang_key:
                    del lang_arr[package_language]
        if lang_arr:
            for item in lang_arr.keys():
                result_summary["language"].append(
                    {
                        "id": LANGUAGE_DICT.get(item),
                        "num": 0,
                        "name": item
                    }
                )

        # 漏洞类型 统计
        vul_type_join = "left JOIN iast_asset_vul_type_relation as typeR on vul.id=typeR.asset_vul_id " \
                        "left JOIN iast_asset_vul_type as typeInfo on typeInfo.id=typeR.asset_vul_type_id "
        count_vul_type_query = "SELECT  typeR.asset_vul_type_id as vul_type_id, count( DISTINCT(vul.id )) AS count_vul_type, " \
                               "typeInfo.name as type_name   from iast_asset_vul as vul  " \
                               + base_join + vul_type_join + query_condition + " group by typeR.asset_vul_type_id  "
        cursor.execute(count_vul_type_query)
        type_summary = cursor.fetchall()
        if type_summary:
            for item in type_summary:
                vul_type_id,count_vul_type,type_name = item
                result_summary['hook_type'].append({
                    "id": vul_type_id,
                    "num": count_vul_type,
                    "name": type_name
                })
        # 归属项目 统计
        count_project_query = "SELECT asset.project_id, count( DISTINCT(vul.id )), " \
                              " asset.project_name from iast_asset_vul as vul  " \
                              + base_join + query_condition + " and asset.project_id>0 group by asset.project_id,asset.project_name  "
        cursor.execute(count_project_query)
        project_summary = cursor.fetchall()
        if project_summary:
            for item in project_summary:
                project_id,count_project,project_name = item
                result_summary['project'].append({
                    "id": project_id,
                    "num": count_project,
                    "name": project_name
                })

    return result_summary


class GetScaSummary(UserEndPoint):
    name = "api-v1-aggregation-summary"
    description = _("New application")

    @extend_schema_with_envcheck(
        request=AggregationArgsSerializer,
        tags=[_('VulList')],
        summary=_('Vul List Select'),
        description=_(
            "count sca vul and app vul by keywords"
        ),
    )
    def post(self, request):
        ser = AggregationArgsSerializer(data=request.data)
        pro_condition = ""
        try:
            if ser.is_valid(True):
                # 从项目列表进入 绑定项目id
                if ser.validated_data.get("bind_project_id", 0):
                    pro_condition = pro_condition + " and asset.project_id={} ".format(
                        str(ser.validated_data.get("bind_project_id")))
                # 项目版本号
                if ser.validated_data.get("project_version_id", 0):
                    pro_condition = pro_condition + " and asset.project_version_id={} ".format(
                        str(ser.validated_data.get("project_version_id")))
        except ValidationError as e:
            return R.failure(data=e.detail)

        if pro_condition:
            # 存在项目筛选条件
            result_summary = get_annotate_sca_common_data(request.user.id,pro_condition)
        else:
            # 全局数据，没有项目信息 数据按用户id缓存
            result_summary = get_annotate_sca_cache_data(request.user.id,pro_condition)

        return R.success(data={
            'messages': result_summary
        }, )
