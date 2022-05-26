
from dongtai_common.models.asset_vul_relation import AssetVulRelation
from dongtai_common.models.aql_info import AqlInfo
from dongtai_common.models.vulnerablity import IastVulnerabilityModel
from dongtai_common.models.agent import IastAgent
from dongtai_common.models.hook_type import HookType
from dongtai_common.models import LICENSE_RISK,SCA_AVAILABILITY_DICT
from dongtai_web.serializers.vul import VulSerializer
from dongtai_common.models import User
from dongtai_common.endpoint import UserEndPoint
from dongtai_common.models.asset_aggr import AssetAggr
from django.db.models import Q

# list id 去重
def getUniqueList(origin_list=[]):
    return list(set(origin_list))

# str to int list
def turnIntListOfStr(type_str,field=""):
    try:
        type_list = type_str.split(",")
        # 安全校验，强制转int
        type_list = list(map(int, type_list))
        if field:
            type_int_list = list(map(str, type_list))
            type_int_str = ",".join(type_int_list)
            return " and {} in ({}) ".format(field,type_int_str)
        else:
            return type_list
    except Exception as e:
        return ""


# 通过sca——aql读取 组件漏洞 修复版本，最新版本，开源许可证,agent_id
def getScaInfoByAql(aql_ids=None):
    if aql_ids is None:
        return {}
    else:
        aql_ids = getUniqueList(aql_ids)
    sca_info = {
        "aql_arr":{},
        "asset_arr":{},
        "hash_arr":{},
        "agent_ids":[]
    }
    aql_info = AqlInfo.objects.filter(id__in=aql_ids).values(
        "id",
        "safe_version","latest_version","source_license","license_risk","availability")
    if aql_info:
        for item in aql_info:
            aql_info_id = str(item['id'])
            del item['id']
            item['license_risk_name'] = LICENSE_RISK.get(str(item['license_risk']),"无风险")
            item['availability_name'] = SCA_AVAILABILITY_DICT.get(str(item['availability']),"无利用信息")
            sca_info["aql_arr"][aql_info_id] = item
    asset_info = AssetVulRelation.objects.filter(aql_info_id__in=aql_ids).values(
        "aql_info_id","id","agent_id","create_time","vul_package_id","hash")
    hash_list = []
    if asset_info:
        for item in asset_info:
            aql_info_id = item['aql_info_id']
            if item['hash'] not in hash_list:
                hash_list.append(item['hash'])
            del item['aql_info_id']
            if not sca_info["asset_arr"].get(aql_info_id):
                sca_info["asset_arr"][aql_info_id] = [item]
            else:
                sca_info["asset_arr"][aql_info_id].append(item)

            sca_info["agent_ids"].append(item['agent_id'])
    # 通过hash list 读取 iast_asset_aggr id
    aggr_info = AssetAggr.objects.filter(signature_value__in=hash_list).values("id","signature_value")

    if aggr_info:
        for item in aggr_info:
            sca_info['hash_arr'][item['signature_value']] = item['id']

    return sca_info

# 通过app vul ids 读取应用漏洞调用链,agent_id，漏洞状态
def getAppVulInfoById(vul_ids=None):
    if vul_ids is None:
        return {}
    vul_info=IastVulnerabilityModel.objects.filter(id__in=vul_ids).values(
        "id",
        "top_stack","bottom_stack","status_id","status__name","agent_id","latest_time")
    vul_result = {
        "vul_info": {},
        "agent_ids":[],
    }
    if vul_info:
        for item in vul_info:
            vul_id = item['id']
            del item['id']
            vul_result['agent_ids'].append(item['agent_id'])
            vul_result['vul_info'][vul_id] = item
    return vul_result

# 通过agent_ids 获取项目id，name，version，中间件，
def getProjectInfoByAgentId(agent_ids=None):
    if agent_ids is None:
        return {}
    else:
        agent_ids = getUniqueList(agent_ids)
    agent_info = IastAgent.objects.filter(id__in=agent_ids).values(
        "id",
        "project_name","project_version_id","project_version__version_name","bind_project_id","server__container"
    )
    agent_result = {}
    if agent_info:
        for item in agent_info:
            agent_id = item['id']
            del item['id']
            item['server_type'] = VulSerializer.split_container_name(
                item['server__container'])
            agent_result[agent_id] = item
    return agent_result

# 通过漏洞类型id 获取漏洞名称，等级
def getHookTypeName(ids=None):
    if ids is None:
        return {}
    else:
        type_arr = {}

    type_info = HookType.objects.filter(id__in=ids).values("id","type","name")
    if type_info:
        for item in type_info:

            type_id = item['id']
            del item['id']
            type_arr[type_id] = item
    return type_arr


# 鉴权  IastVulAssetRelation
def getAuthUserInfo(user,base_query):
    # is_superuser == 2 租户管理员 is_superuser == 1 超级管理员  is_department_admin==True 部门管理员  其他为普通用户
    user_id = user.id
    # 超级管理员
    if user.is_system_admin():
        base_query = base_query.filter(asset__user_id=user_id)
    # 租户管理员 获取 租户id
    elif user.is_talent_admin():
        talent = user.get_talent()
        if not talent or talent is None:
            base_query = base_query.filter(asset__user_id=user_id)
        else:
            base_query = base_query.filter(asset__talent_id=talent.id)
    # 部门管理员 获取部门id
    elif user.is_department_admin:
        users = UserEndPoint.get_auth_users(user)
        user_ids = list(users.values_list("id", flat=True))
        base_query = base_query.filter(asset__user_id__in=user_ids)
    else:
        # 普通用户，直接筛选用户id
        base_query = base_query.filter(asset__user_id=user_id)
    return base_query


def auth_user_list_str(user=None,user_id=0,user_table=""):
    result = {
        "user_list":[],
        "user_str":"",
        "user_condition_str":""
    }
    if user is None:
        user = User.objects.filter(id=user_id).first()
    users = UserEndPoint.get_auth_users(user)
    user_ids = list(users.values_list("id", flat=True))
    result['user_list'] = user_ids
    user_ids_arr = list(map(str, user_ids))
    user_str = ",".join(user_ids_arr)
    result['user_str'] = user_str
    if user_table:
        result['user_condition_str'] = " and {}.user_id in ({})".format(user_table, user_str)

    return  result


# 鉴权 后 获取 漏洞信息  auth_condition = getAuthBaseQuery(request.user, "asset")
def getAuthBaseQuery(user=None,table_str="",user_id=0):

    # is_superuser == 2 租户管理员 is_superuser == 1 超级管理员  is_department_admin==True 部门管理员  其他为普通用户
    if user is None:
        user = User.objects.filter(id=user_id).first()
    else:
        user_id = user.id

    query_base = " and {}.user_id={}".format(table_str, user_id)
    # 超级管理员
    if user.is_system_admin():
        query_base = ""
    # 租户管理员 获取 租户id
    elif user.is_talent_admin():
        talent = user.get_talent()
        if not talent or talent is None:
            pass
        else:
            query_base = " and {}.talent_id={}".format(table_str,talent.id)
    # 部门管理员 获取部门id
    elif user.is_department_admin:
        users = UserEndPoint.get_auth_users(user)
        user_ids = list(users.values_list("id", flat=True))
        user_ids = list(map(str, user_ids))
        user_str = ",".join(user_ids)
        query_base = " and {}.user_id in ({})".format(table_str,user_str)

    return query_base
