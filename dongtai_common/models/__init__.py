#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/25 下午6:43
# software: PyCharm
# project: dongtai-models

from .user import User
from . import api_route
LANGUAGE_DICT = {'JAVA': 1, 'PYTHON': 2, 'PHP': 3, 'GO': 4}
### aggregation
LANGUAGE_ID_DICT = {"1":"JAVA", "2": "PYTHON", "3": "PHP", "4":"GO"}
AVAILABILITY_DICT = {
    "1": "存在利用代码",
    "2": "存在分析文章",
    "3": "无利用信息",
}
SOURCE_TYPE_DICT = {
    "1": "应用漏洞",
    "2": "组件漏洞"
}
AGGREGATION_ORDER = {
    "1":"vul.level_id",
    "2":"rel.create_time",
    "3":"vul.update_time",
}

APP_VUL_ORDER = {
    "1":"level_id",
    "2":"first_time",
    "3":"latest_time",
    "4":"status_id",
}
#license 风险等级
LICENSE_RISK = {
    "1": "高",
    "2": "中",
    "3": "低",
    "0": "无风险",
}
# 漏洞等级
APP_LEVEL_RISK = {
    "1": "高危",
    "2": "中危",
    "3": "低危",
    "4": "无风险",
    "5": "提示",
}
# 组件漏洞可利用性
SCA_AVAILABILITY_DICT = {
    "1":"存在利用代码",
    "2":"存在分析文章",
    "3":"无利用信息"
}
# default share config key
SHARE_CONFIG_DICT={
    "jira_url":"",
    "jira_id":"",
    "gitlab_url":"",
    "gitlab_id":"",
    "zendao_url":"",
    "zendao_id":""
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
### end
WHITE_DOMAIN_NOTIFY = [
    "open.feishu.cn",
    "qyapi.weixin.qq.com",
    "oapi.dingtalk.com"
]