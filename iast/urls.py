#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/5/21 15:55
# software: PyCharm
# project: webapi
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from iast.account.department import DepartmentEndPoint
from iast.account.talent import TalentEndPoint
from iast.account.user import UserEndPoint
from iast.views.agent_delete import AgentDeleteEndPoint
from iast.views.agent_deploy_doc import AgentDeployDesc
from iast.views.agent_deploy_info import AgentDeployInfo
from iast.views.agent_deploy_submit import AgentDeploySave
from iast.views.agent_download import AgentDownload
from iast.views.agent_install import AgentInstall
from iast.views.agent_uninstall import AgentUninstall
from iast.views.agent_upgrade_offline import AgentUpgradeOffline
from iast.views.agent_upgrade_online import AgentUpgradeOnline
from iast.views.agents import AgentList
from iast.views.agents_user import UserAgentList
from iast.views.captcha_create import CaptchaCreate
from iast.views.engine_hook_rule_add import EngineHookRuleAddEndPoint
from iast.views.engine_hook_rule_delete import EngineHookRuleDeleteEndPoint
from iast.views.engine_hook_rule_disable import EngineHookRuleDisableEndPoint
from iast.views.engine_hook_rule_enable import EngineHookRuleEnableEndPoint
from iast.views.engine_hook_rule_modify import EngineHookRuleModifyEndPoint
from iast.views.engine_hook_rule_summary import EngineHookRuleSummaryEndPoint
from iast.views.engine_hook_rule_type_add import EngineHookRuleTypeAddEndPoint
from iast.views.engine_hook_rule_type_disable import EngineHookRuleTypeDisableEndPoint
from iast.views.engine_hook_rule_type_enable import EngineHookRuleTypeEnableEndPoint
from iast.views.engine_hook_rule_types import EngineHookRuleTypesEndPoint
from iast.views.engine_hook_rules import EngineHookRulesEndPoint
from iast.views.engine_method_pool_detail import MethodPoolDetailProxy
from iast.views.engine_vul_rule import EngineVulRuleEndPoint
from iast.views.engine_vul_rule_detail import EngineVulRuleDetailEndPoint
from iast.views.engine_vul_rule_save import EngineVulRuleSaveEndPoint
from iast.views.engine_vul_rule_type import EngineVulRuleTypeEndPoint
from iast.views.log_clear import LogClear
from iast.views.log_delete import LogDelete
from iast.views.log_export import LogExport
from iast.views.logs import LogsEndpoint
from iast.views.engine_method_pool_search import MethodPoolSearchProxy
from iast.views.engine_method_pools import MethodPoolProxy
from iast.views.openapi import OpenApiEndpoint
from iast.views.project_add import ProjectAdd
from iast.views.project_delete import ProjectDel
from iast.views.project_detail import ProjectDetail
from iast.views.project_engines import ProjectEngines
from iast.views.project_report_export import ProjectReportExport
from iast.views.project_summary import ProjectSummary
from iast.views.projects import Projects
from iast.views.sca_details import ScaDetailView
from iast.views.sca_sidebar_index import ScaSidebarList
from iast.views.sca_summary import ScaSummary
from iast.views.scas import ScaList
from iast.views.strategy_disable import StrategyDisableEndpoint
from iast.views.strategy_enable import StrategyEnableEndpoint
from iast.views.strategys import StrategyEndpoint
from iast.views.strategys_add import StrategyAdd
from iast.views.strategys_list import StrategyList
from iast.views.strategys_type import StrategyType
from iast.views.system_info import SystemInfo
from iast.views.user_detail import UserDetailEndPoint
from iast.views.user_info import UserInfoEndpoint
from iast.views.user_login import UserLogin
from iast.views.user_logout import UserLogout
from iast.views.user_passwrd import UserPassword
from iast.views.user_token import UserToken
from iast.views.vuln_delete import VulnDelete
from iast.views.vuln_details import VulnDetail
from iast.views.vuln_index import VulnList
from iast.views.vuln_sidebar_index import VulnSideBarList
from iast.views.vuln_summary import VulnSummary

urlpatterns = [
    # 租户管理 - 系统管理员
    path("talents", TalentEndPoint.as_view()),
    path("talent/<int:pk>", TalentEndPoint.as_view()),
    path("talent/add", TalentEndPoint.as_view()),
    path("talent/<int:pk>/delete", TalentEndPoint.as_view()),

    # 部门管理（支持多级） - 系统管理员 - 考虑多级部门的实现
    path('departments', DepartmentEndPoint.as_view()),
    path('department/<int:pk>', DepartmentEndPoint.as_view()),
    path('department/add', DepartmentEndPoint.as_view()),
    path('department/<int:pk>/delete', DepartmentEndPoint.as_view()),

    # 用户管理 - 租户管理员/系统管理员 - 创建用户、修改密码、登录、登出、获取token
    # todo
    path('users', UserEndPoint.as_view()),
    path('user/add', UserEndPoint.as_view()),
    path('user/<int:user_id>/delete', UserEndPoint.as_view()),
    path('user/<int:user_id>', UserEndPoint.as_view()),
    path('user/<int:user_id>', UserDetailEndPoint.as_view()),
    path('user/changePassword', UserPassword.as_view()),
    path('user/login', UserLogin.as_view()),
    path('user/logout', UserLogout.as_view()),
    path('user/info', UserInfoEndpoint.as_view()),
    path('user/token', UserToken.as_view()),

    # 验证码相关
    path('captcha/', include('captcha.urls')),
    path(r'captcha/refresh', CaptchaCreate.as_view()),

    # 项目接口
    path('project/<int:id>', ProjectDetail.as_view()),
    path('project/add', ProjectAdd.as_view()),
    path('project/delete', ProjectDel.as_view()),
    path('projects', Projects.as_view()),
    path('projects/summary/<int:id>', ProjectSummary.as_view()),
    path('project/engines/<int:pid>', ProjectEngines.as_view()),
    path('project/export', ProjectReportExport.as_view()),
    # 漏洞接口：漏洞列表、漏洞信息总览、漏洞详情侧边栏、漏洞详情
    path('vulns', VulnList.as_view()),
    path('vuln/summary', VulnSummary.as_view()),
    path('vuln/list', VulnSideBarList.as_view()),
    path('vuln/<int:id>', VulnDetail.as_view()),
    path('vuln/delete/<int:id>', VulnDelete.as_view()),
    # 三方组件接口：组件列表、组件信息总览、组件详情侧边栏、组件详情
    path('scas', ScaList.as_view()),
    path('sca/summary', ScaSummary.as_view()),
    path('sca/list', ScaSidebarList.as_view()),
    path('sca/<int:id>', ScaDetailView.as_view()),
    # 策略列表接口
    path('strategys', StrategyEndpoint.as_view()),
    path('strategy/<int:id>/enable', StrategyEnableEndpoint.as_view()),
    path('strategy/<int:id>/disable', StrategyDisableEndpoint.as_view()),
    # 获取 按类型获取策略信息
    path('strategy/types', StrategyType.as_view()),
    # 用户创建策略
    path('strategy/user/add', StrategyAdd.as_view()),
    # 用户查询自有策略
    path('strategy/user/list', StrategyList.as_view()),
    # 新增项目捆绑策略
    # agent相关接口：下载agent、下载自动化部署工具、部署文档、agent列表、安装agent、卸载agent、在线升级、离线升级
    path('agent/deploy/doc', AgentDeployDesc.as_view()),
    path('agent/deploy/info', AgentDeployInfo.as_view()),
    path('agent/deploy/submit', AgentDeploySave.as_view()),
    path('agents', AgentList.as_view()),
    path('agent/<int:pk>/delete', AgentDeleteEndPoint.as_view()),
    path('agents/user', UserAgentList.as_view()),
    path('agent/install', AgentInstall.as_view()),
    path('agent/uninstall', AgentUninstall.as_view()),
    path('agent/upgrade/online', AgentUpgradeOnline.as_view()),
    path('agent/upgrade/offline', AgentUpgradeOffline.as_view()),
    path('agent/download', AgentDownload.as_view()),

    # 获取openapi地址
    path('openapi', OpenApiEndpoint.as_view()),

    # 系统信息
    path('system/info', SystemInfo.as_view()),
    # 日志信息
    path('logs', LogsEndpoint.as_view()),
    path('log/export', LogExport.as_view()),
    path('log/delete', LogDelete.as_view()),
    path('log/clear', LogClear.as_view()),

    # 方法池相关
    # path('method_pools', MethodPoolProxy.as_view()),
    path('engine/method_pool/search', MethodPoolSearchProxy.as_view()),
    path('engine/method_pool/detail', MethodPoolDetailProxy.as_view()),
    path('engine/vul_rule', EngineVulRuleEndPoint.as_view()),
    # /api/engine/rule/type
    path('engine/vul_rule/type', EngineVulRuleTypeEndPoint.as_view()),
    path('engine/vul_rule/detail', EngineVulRuleDetailEndPoint.as_view()),
    path('engine/vul_rule/save', EngineVulRuleSaveEndPoint.as_view()),
    # hook规则相关
    path('engine/hook/rule/summary', EngineHookRuleSummaryEndPoint.as_view()),
    path('engine/hook/rule/add', EngineHookRuleAddEndPoint.as_view()),
    path('engine/hook/rule/modify', EngineHookRuleModifyEndPoint.as_view()),
    path('engine/hook/rule/enable', EngineHookRuleEnableEndPoint.as_view()),
    path('engine/hook/rule/disable', EngineHookRuleDisableEndPoint.as_view()),
    path('engine/hook/rule/delete', EngineHookRuleDeleteEndPoint.as_view()),
    path('engine/hook/rule_type/add', EngineHookRuleTypeAddEndPoint.as_view()),
    path('engine/hook/rule_type/disable', EngineHookRuleTypeDisableEndPoint.as_view()),
    path('engine/hook/rule_type/enable', EngineHookRuleTypeEnableEndPoint.as_view()),
    path('engine/hook/rule_types', EngineHookRuleTypesEndPoint.as_view()),
    path('engine/hook/rules', EngineHookRulesEndPoint.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
