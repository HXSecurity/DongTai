#!/usr/bin/env python
# datetime:2021/1/25 下午6:43

from .user import User
from . import api_route

LANGUAGE_DICT = {"JAVA": 1, "PYTHON": 2, "PHP": 3, "GO": 4}
# aggregation
LANGUAGE_ID_DICT = {"1": "JAVA", "2": "PYTHON", "3": "PHP", "4": "GO"}
AVAILABILITY_DICT = {
    "1": "存在利用代码",
    "2": "存在分析文章",
    "3": "无利用信息",
}
SOURCE_TYPE_DICT = {"1": "应用漏洞", "2": "组件漏洞"}
AGGREGATION_ORDER = {
    "1": "vul.level_id",
    "2": "vul.create_time",
    "3": "vul.update_time",
}

APP_VUL_ORDER = {
    "1": "level_id",
    "2": "first_time",
    "3": "latest_time",
    "4": "status_id",
}
# license 风险等级
LICENSE_RISK = {
    "1": "高",
    "2": "中",
    "3": "低",
    "0": "无风险",
    "4": "无风险",
}
LICENSE_RISK_DESC = {
    "1": "禁止商业闭源集成",
    "2": "限制性商业闭源集成",
    "3": "部分商业闭源集成",
    "0": "无商业闭源集成",
    "4": "无商业闭源集成",
}
# 漏洞等级
APP_LEVEL_RISK = {"1": "高危", "2": "中危", "3": "低危", "4": "无风险", "5": "提示", "0": "无风险"}
# 图片生成
PNG_TREND_LEVEL = {"1": "高危漏洞", "2": "中危漏洞", "3": "低危漏洞", "4": "提示信息"}
# 组件漏洞可利用性
SCA_AVAILABILITY_DICT = {"1": "存在利用代码", "2": "存在分析文章", "3": "无利用信息"}
# default share config key
SHARE_CONFIG_DICT = {
    "jira_url": "",
    "jira_id": "",
    "gitlab_url": "",
    "gitlab_id": "",
    "zendao_url": "",
    "zendao_id": "",
}

NOTIFY_TYPE_DICT = {
    "1": "webHook",
    "2": "GitLab",
    "3": "Jira",
    "4": "ZenDao",
    "5": "FeiShu",
    "6": "WeiXin",
    "7": "DingDing",
}
# end
WHITE_DOMAIN_NOTIFY = ["open.feishu.cn", "qyapi.weixin.qq.com", "oapi.dingtalk.com"]

VUL_TYPE_CSS = {
    "1": "sca-height",
    "2": "sca-middle",
    "3": "sca-low",
    "4": "sca-info",
}

VUL_DEP_CSS = {
    "1": "height",
    "2": "middle",
    "3": "low",
    "4": "info",
}

# export report default info
DEFAULT_EXPORT_REPORT_DICT = {
    "description": {
        "user_id": "user_id",
        "report_name": "report_name",
        "project_name": "",
        "version_name": "version_name",
        "api_vount": "",
        "vul_level_count": {},
        "license_level_count": {},
        "project_create_time": "",
        "report_create_time": "",
    },
    "risk_analysis": {
        "content": "",
        "level_png": "",
        "trend_png": "",
        "app_vul_type": {
            "1": {},
            "2": {},
            "3": {},
            "4": {},
            "5": {},
        },
        "sca_vul_type": {
            "1": {},
            "2": {},
            "3": {},
            "4": {},
            "5": {},
        },
        "license_type": {},
    },
    "risk_details": {
        "app_vul_detail": [],
        "sca_vul_detail": [],
        "license_vul_detail": [],
    },
    "sca_list": {},
    "api_site_map": {},
}
