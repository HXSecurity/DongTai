# 按类型获取 组件漏洞 应用漏洞列表
import json,time,logging
from dongtai_common.endpoint import R
from django.forms import model_to_dict
from dongtai_common.endpoint import UserEndPoint

from dongtai_web.utils import extend_schema_with_envcheck
from dongtai_web.serializers.aggregation import AggregationArgsSerializer
from rest_framework.serializers import ValidationError
from django.utils.translation import gettext_lazy as _
from dongtai_web.aggregation.aggregation_common import getAuthUserInfo, turnIntListOfStr, getAuthBaseQuery, auth_user_list_str
import pymysql
from dongtai_web.serializers.vul import VulSerializer
from dongtai_common.models.asset_vul import IastAssetVul,IastVulAssetRelation,IastAssetVulType,IastAssetVulTypeRelation
from dongtai_common.models import AGGREGATION_ORDER, LANGUAGE_ID_DICT, SHARE_CONFIG_DICT, APP_LEVEL_RISK, LICENSE_RISK, \
    SCA_AVAILABILITY_DICT


logger = logging.getLogger("django")


class GetAggregationVulList(UserEndPoint):
    name = "api-v1-aggregation-vul-list"
    description = _("New application")

    @extend_schema_with_envcheck(
        request=AggregationArgsSerializer,
        tags=[_('VulList')],
        summary=_('Vul List Select'),
        description=_(
            "select sca vul and app vul by keywords"
        ),
    )
    # 组件漏洞 列表
    def post(self, request):
        ser = AggregationArgsSerializer(data=request.data)
        keywords = ""
        join_table = ""
        query_condition = " where rel.is_del=0 "
        try:
            if ser.is_valid(True):
                page_size = ser.validated_data['page_size']
                page = ser.validated_data['page']
                begin_num = (page - 1) * page_size
                end_num = page * page_size

                keywords = ser.validated_data.get("keywords", "")
                if keywords:
                    keywords = pymysql.converters.escape_string(keywords)
                    keywords = "+" + keywords

                order_type = AGGREGATION_ORDER.get(str(ser.validated_data['order_type']), "vul.level_id")
                order_type_desc = "desc" if ser.validated_data['order_type_desc'] else "asc"
                # 从项目列表进入 绑定项目id
                if ser.validated_data.get("bind_project_id", 0):
                    query_condition = query_condition + " and asset.project_id={} ".format(str(ser.validated_data.get("bind_project_id")))
                # 项目版本号
                if ser.validated_data.get("project_version_id", 0):
                    query_condition = query_condition + " and asset.project_version_id={} ".format(str(ser.validated_data.get("project_version_id")))
                # 按项目筛选
                if ser.validated_data.get("project_id_str", ""):
                    project_str = turnIntListOfStr(ser.validated_data.get("project_id_str", ""),"asset.project_id")
                    query_condition = query_condition + project_str
                # 按语言筛选
                if ser.validated_data.get("language_str", ""):
                    language_str = ser.validated_data.get("language_str", "")
                    type_list = language_str.split(",")
                    # 安全校验，强制转int
                    type_list = list(map(int, type_list))
                    type_int_list = list(map(str, type_list))
                    lang_str = []
                    for one_type in type_int_list:
                        lang_str.append("'"+LANGUAGE_ID_DICT.get(one_type,"")+"'")
                    type_int_str = ",".join(lang_str)
                    language_str_change = " and {} in ({}) ".format("vul.package_language", type_int_str)
                    query_condition = query_condition + language_str_change
                # 漏洞类型筛选
                if ser.validated_data.get("hook_type_id_str", ""):
                    vul_type_str = turnIntListOfStr(ser.validated_data.get("hook_type_id_str", ""), "typeR.asset_vul_type_id")
                    query_condition = query_condition + vul_type_str
                    join_table = join_table + "left JOIN iast_asset_vul_type_relation as typeR on vul.id=typeR.asset_vul_id "
                # 漏洞等级筛选
                if ser.validated_data.get("level_id_str", ""):
                    status_str = turnIntListOfStr(ser.validated_data.get("level_id_str", ""), "vul.level_id")
                    query_condition = query_condition + status_str
                # 可利用性
                if ser.validated_data.get("availability_str", ""):
                    availability_arr = turnIntListOfStr(ser.validated_data.get("availability_str", ""))
                    if 3 in availability_arr:
                        query_condition = query_condition + " and vul.have_article=0 and vul.have_poc=0 "
                    else:
                        if 1 in availability_arr:
                            query_condition = query_condition + " and vul.have_poc=1 "
                        if 2 in availability_arr:
                            query_condition = query_condition + " and vul.have_article=1 "

        except ValidationError as e:
            return R.failure(data=e.detail)
        user_auth_info = auth_user_list_str(user=request.user,user_table="asset")
        query_condition = query_condition + user_auth_info.get("user_condition_str")

        if keywords:
            query_base = "SELECT DISTINCT(vul.id),vul.*,rel.create_time, " \
                " MATCH( `vul`.`vul_name`,`vul`.`aql`,`vul`.`vul_serial` ) AGAINST ( %s IN NATURAL LANGUAGE MODE ) AS `score`" \
                "  from  iast_asset_vul_relation as rel   " \
                "left JOIN iast_asset_vul as vul on rel.asset_vul_id=vul.id  " \
                "left JOIN iast_asset as asset on rel.asset_id=asset.id  " + join_table + query_condition

        else:
            query_base = "SELECT DISTINCT(vul.id),vul.*,rel.create_time from  iast_asset_vul_relation as rel   " \
                        "left JOIN iast_asset_vul as vul on rel.asset_vul_id=vul.id  " \
                        "left JOIN iast_asset as asset on rel.asset_id=asset.id  " + join_table + query_condition

        # mysql 全文索引下，count不准确，等于全部数量
        new_order = order_type+ " " + order_type_desc
        if order_type == "vul.level_id":
            if order_type_desc == "desc":
                new_order  = new_order +  ", vul.update_time desc"
            else:
                new_order = new_order + ", vul.update_time_desc"

        if keywords:
            all_vul = IastAssetVul.objects.raw(query_base + "  order by score desc, %s limit %s,%s;  " % (new_order,  begin_num, end_num),[keywords])
        else:
            all_vul = IastAssetVul.objects.raw(query_base + "  order by %s  limit %s,%s;  " % (new_order, begin_num, end_num))
        content_list = []
        print(all_vul.query)
        if all_vul:
            vul_ids = []
            # print(all_vul.query.__str__())
            for item in all_vul:
                # 拼写 漏洞类型
                # 拼写 漏洞编号
                availability_arr = []
                if item.have_poc:
                    availability_arr.append(SCA_AVAILABILITY_DICT.get("1"))
                if item.have_article:
                    availability_arr.append(SCA_AVAILABILITY_DICT.get("2"))
                if not availability_arr:
                    availability_arr.append(SCA_AVAILABILITY_DICT.get("3"))
                availability_str = ",".join(availability_arr)
                cur_data = {
                    "id": item.id,
                    "vul_name": item.vul_name,
                    "create_time": item.create_time,
                    "level_id": item.level_id,
                    "level_name": APP_LEVEL_RISK.get(str(item.level_id),""),
                    "license": item.license,
                    "license_level": item.license_level,
                    "license_risk_name": LICENSE_RISK.get(str(item.license_level),"") ,
                    "vul_cve_nums": item.vul_cve_nums,
                    "package_name": item.aql,
                    "package_safe_version": item.package_safe_version,
                    "package_latest_version": item.package_latest_version,
                    "package_language": item.package_language,
                    # "type_id": item.type_id,
                    "availability_str": availability_str,
                    # "type_name": item.type_name,
                }
                cwe = cur_data.get("vul_cve_nums",{}).get("cwe","").replace("CWE-","")
                if cwe:
                    cur_data['vul_cve_nums']['cwe_num'] = cwe
                vul_ids.append(item.id)
                content_list.append(cur_data)
            # 追加 用户 权限
            base_relation = IastVulAssetRelation.objects.filter(
                asset_vul_id__in=vul_ids,is_del=0,asset__user_id__in=user_auth_info['user_list'],asset__project_id__gt=0)
            # base_relation = getAuthUserInfo(request.user,base_relation)
            pro_info = base_relation.values(
                "asset_vul_id","asset__project_id","asset__project_name","asset__project_version__version_name","asset__agent__server__container"
            ).order_by("-create_time")
            pro_arr = {}
            for item in pro_info:
                vul_id = item['asset_vul_id']
                item['server_type'] = VulSerializer.split_container_name(item['asset__agent__server__container'])
                del item['asset_vul_id']
                if pro_arr.get(vul_id,[]):
                    pro_arr[vul_id].append(item)
                else:
                    pro_arr[vul_id] = [item]
            # 根据vul_id获取对应的漏洞类型 一对多
            type_info = IastAssetVulTypeRelation.objects.filter(asset_vul_id__in=vul_ids).values(
                "asset_vul_id", "asset_vul_type__name")
            type_arr = {}
            for item in type_info:
                if not type_arr.get(item['asset_vul_id'],[]):
                    type_arr[item['asset_vul_id']] = [item['asset_vul_type__name']]
                elif item['asset_vul_type__name'] not in type_arr[item['asset_vul_id']]:
                    type_arr[item['asset_vul_id']].append(item['asset_vul_type__name'])
            for row in content_list:
                row["pro_info"] = pro_arr.get(row['id'], [])
                row['type_name'] = ",".join(type_arr.get(row['id'], []))
        return R.success(data={
            'messages': content_list,
            'page': {
                "page_size":page_size,
                "cur_page":page
            }
        }, )
