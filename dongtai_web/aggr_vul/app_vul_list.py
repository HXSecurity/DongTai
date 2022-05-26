from rest_framework.serializers import ValidationError
from dongtai.endpoint import R
from dongtai.endpoint import UserEndPoint
from dongtai.models.vulnerablity import IastVulnerabilityModel
from dongtai_web.aggregation.aggregation_common import turnIntListOfStr,auth_user_list_str
from dongtai_web.serializers.vul import VulSerializer
from django.utils.translation import gettext_lazy as _
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer
from dongtai.models.vulnerablity import IastVulnerabilityStatus
import pymysql
from dongtai_web.serializers.aggregation import AggregationArgsSerializer
from dongtai.models import AGGREGATION_ORDER,LANGUAGE_ID_DICT,APP_LEVEL_RISK,APP_VUL_ORDER
from django.db.models import F
from dongtai.utils.db import SearchLanguageMode


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
        queryset = IastVulnerabilityModel.objects.filter(is_del=0,agent__user_id__in=auth_user_info['user_list'])

        try:
            if ser.is_valid(True):
                page_size = ser.validated_data['page_size']
                page = ser.validated_data['page']
                begin_num = (page - 1) * page_size
                end_num = page * page_size
                keywords = ser.validated_data.get("keywords", "")
                # 从项目列表进入 绑定项目id
                if ser.validated_data.get("bind_project_id", 0):
                    queryset = queryset.filter(agent__bind_project_id=ser.validated_data.get("bind_project_id"))
                # 项目版本号
                if ser.validated_data.get("project_version_id", 0):
                    queryset = queryset.filter(agent__project_version_id=ser.validated_data.get("project_version_id"))
                # 按项目筛选
                if ser.validated_data.get("project_id_str", ""):
                    project_id_list = turnIntListOfStr(ser.validated_data.get("project_id_str", ""))
                    queryset = queryset.filter(agent__bind_project_id__in=project_id_list)
                # 漏洞类型筛选
                if ser.validated_data.get("hook_type_id_str", ""):
                    vul_type_list = turnIntListOfStr(ser.validated_data.get("hook_type_id_str", ""))
                    queryset = queryset.filter(strategy_id__in=vul_type_list)
                # 漏洞等级筛选
                if ser.validated_data.get("level_id_str", ""):
                    level_id_list = turnIntListOfStr(ser.validated_data.get("level_id_str", ""))
                    queryset = queryset.filter(level_id__in=level_id_list)
                # 按状态筛选
                if ser.validated_data.get("status_id_str", ""):
                    status_id_list = turnIntListOfStr(ser.validated_data.get("status_id_str", ""))
                    queryset = queryset.filter(status_id__in=status_id_list)
                # 按语言筛选
                if ser.validated_data.get("language_str", ""):
                    language_id_list = turnIntListOfStr(ser.validated_data.get("language_str", ""))
                    language_arr = []
                    for lang in language_id_list:
                        language_arr.append(LANGUAGE_ID_DICT.get(str(lang)))
                    queryset = queryset.filter(agent__language__in=language_arr)

                order_list = []
                fields = ["id", "uri","http_method","top_stack","bottom_stack","level_id",
                            "taint_position","status_id","first_time","latest_time", "strategy__vul_name","agent__language",
                            "agent__project_name","agent__server__container","agent__bind_project_id"
                            ]
                if keywords:
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

        return R.success(data={
            'messages': end['data'],
            'page': {
                "page_size": page_size,
                "cur_page": page
            }
        }, )
