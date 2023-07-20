from dongtai_common.endpoint import UserEndPoint
from dongtai_common.models import User
from dongtai_common.models.agent import IastAgent
from dongtai_common.models.hook_type import HookType
from dongtai_common.models.vulnerablity import IastVulnerabilityModel
from dongtai_web.serializers.vul import VulSerializer


# list id 去重
def getUniqueList(origin_list=[]):
    return list(set(origin_list))


# str to int list
def turnIntListOfStr(type_str, field=""):
    try:
        type_list = type_str.split(",")
        # 安全校验,强制转int
        type_list = list(map(int, type_list))
        if field:
            type_int_list = list(map(str, type_list))
            type_int_str = ",".join(type_int_list)
            return f" and {field} in ({type_int_str}) "
        return type_list
    except Exception:
        return ""


# str 逗号分割,强校验
def checkMustIntToStr(type_str):
    type_list = type_str.split(",")

    if not type_list or not type_str:
        return ""
    # 去重
    type_arr = list(set(type_list))
    # 转int

    type_int_list = list(map(int, type_arr))
    # 转 str
    type_str_list = list(map(str, type_int_list))
    return ",".join(type_str_list)


# 通过app vul ids 读取应用漏洞调用链,agent_id,漏洞状态
def getAppVulInfoById(vul_ids=None):
    if vul_ids is None:
        return {}
    vul_info = IastVulnerabilityModel.objects.filter(id__in=vul_ids).values(
        "id",
        "top_stack",
        "bottom_stack",
        "status_id",
        "status__name",
        "agent_id",
        "latest_time",
    )
    vul_result = {
        "vul_info": {},
        "agent_ids": [],
    }
    if vul_info:
        for item in vul_info:
            vul_id = item["id"]
            del item["id"]
            vul_result["agent_ids"].append(item["agent_id"])
            vul_result["vul_info"][vul_id] = item
    return vul_result


# 通过agent_ids 获取项目id,name,version,中间件,
def getProjectInfoByAgentId(agent_ids=None):
    if agent_ids is None:
        return {}
    agent_ids = getUniqueList(agent_ids)
    agent_info = IastAgent.objects.filter(id__in=agent_ids).values(
        "id",
        "project_name",
        "project_version_id",
        "project_version__version_name",
        "bind_project_id",
        "server__container",
    )
    agent_result = {}
    if agent_info:
        for item in agent_info:
            agent_id = item["id"]
            del item["id"]
            item["server_type"] = VulSerializer.split_container_name(
                item["server__container"]
            )
            agent_result[agent_id] = item
    return agent_result


# 通过漏洞类型id 获取漏洞名称,等级
def getHookTypeName(ids=None):
    if ids is None:
        return {}
    type_arr = {}

    type_info = HookType.objects.filter(id__in=ids).values("id", "type", "name")
    if type_info:
        for item in type_info:
            type_id = item["id"]
            del item["id"]
            type_arr[type_id] = item
    return type_arr


# 应用漏洞推送
def appVulShareConfig(app_vul_ids, user_id):
    return {}


#        user_id=user_id).values("vul_id", "jira_url", "jira_id", "gitlab_url",
#                                "gitlab_id", "zendao_url", "zendao_id")
#    if query_vul_inetration:
#        for item in query_vul_inetration:


# 鉴权  IastVulAssetRelation
def getAuthUserInfo(user, base_query):
    # Don't use it again.
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
        # 普通用户,直接筛选用户id
        base_query = base_query.filter(asset__user_id=user_id)
    return base_query


def auth_user_list_str(user=None, user_id=0, user_table=""):
    # Don't use it again.
    result = {"user_list": [], "user_str": "", "user_condition_str": ""}
    if user is None:
        user = User.objects.filter(id=user_id).first()
    if not user:
        return result
    departments = user.get_relative_department()
    department_ids = list(departments.values_list("id", flat=True))
    department_ids_arr = ",".join(list(map(str, department_ids)))
    user_ids = list(
        User.objects.filter(department__in=departments).values_list("id", flat=True)
    )
    result["user_list"] = user_ids
    user_ids_arr = list(map(str, user_ids))
    user_str = ",".join(user_ids_arr)
    result["user_str"] = user_str
    result["department_list"] = department_ids
    result["department_str"] = department_ids_arr
    if user_table:
        result["user_condition_str"] = " and {}.department_id in ({})".format(
            user_table, department_ids_arr
        )
    return result


def auth_user_list_only(user_id=0):
    user = User.objects.filter(id=user_id).first()
    if not user:
        return []
    users = UserEndPoint.get_auth_users(user)
    return list(users.values_list("id", flat=True))


# 鉴权 后 获取 漏洞信息  auth_condition = getAuthBaseQuery(request.user, "asset")
def getAuthBaseQuery(user=None, table_str="", user_id=0):
    # Don't use it again.

    # is_superuser == 2 租户管理员 is_superuser == 1 超级管理员  is_department_admin==True 部门管理员  其他为普通用户
    if user is None:
        user = User.objects.filter(id=user_id).first()
    else:
        user_id = user.id

    query_base = f" and {table_str}.user_id={user_id}"
    # 超级管理员
    if user.is_system_admin():
        query_base = ""
    # 租户管理员 获取 租户id
    elif user.is_talent_admin():
        talent = user.get_talent()
        if not talent or talent is None:
            pass
        else:
            query_base = f" and {table_str}.talent_id={talent.id}"
    # 部门管理员 获取部门id
    elif user.is_department_admin:
        users = UserEndPoint.get_auth_users(user)
        user_ids = list(users.values_list("id", flat=True))
        user_ids = list(map(str, user_ids))
        user_str = ",".join(user_ids)
        query_base = f" and {table_str}.user_id in ({user_str})"

    return query_base
