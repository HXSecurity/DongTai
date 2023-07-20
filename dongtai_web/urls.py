#!/usr/bin/env python
# -*- coding:utf-8 -*-
# datetime:2020/5/21 15:55
from dongtai_web.systemmonitor.urls import urlpatterns as systemmonitor_urls
from dongtai_web.versioncontrol.urls import urlpatterns as versioncontrol_urls
from dongtai_web.dongtai_sca.urls import urlpatterns as sca_urls
from dongtai_web.apitimelog.urls import urlpatterns as apitimelog_urls
from dongtai_web.scaupload.urls import urlpatterns as scaupload_urls
from dongtai_web.aggr_vul.app_vul_summary import GetAppVulsSummary
from dongtai_web.aggr_vul.app_vul_list import GetAppVulsList
from dongtai_web.aggr_vul.aggr_vul_summary import GetScaSummary
from dongtai_web.aggr_vul.aggr_vul_list import GetAggregationVulList
from dongtai_web.views.agents_v2 import AgentListv2
import os
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from dongtai_web.base.update_project_version import UpdateProjectVersion
from dongtai_web.views.agent_delete import AgentDeleteEndPoint
from dongtai_web.views.agent_deploy import AgentDeploy
from dongtai_web.views.agent_install import AgentInstall
from dongtai_web.views.agent_start import AgentStart
from dongtai_web.views.agent_status_update import AgentStatusUpdate
from dongtai_web.views.agents_delete import AgentsDeleteEndPoint
from dongtai_web.views.agent_stop import AgentStop
from dongtai_web.views.agent_uninstall import AgentUninstall
from dongtai_web.views.agent import Agent
from dongtai_web.views.agents import AgentList
from dongtai_web.views.agents_user import UserAgentList
from dongtai_web.views.agent_summary import AgentSummary
from dongtai_web.views.captcha_create import CaptchaCreate
from dongtai_web.views.documents import DocumentsEndpoint
from dongtai_web.views.engine_hook_rule_add import EngineHookRuleAddEndPoint
from dongtai_web.views.engine_hook_rule_modify import EngineHookRuleModifyEndPoint
from dongtai_web.views.engine_hook_rule_status import EngineHookRuleEnableEndPoint
from dongtai_web.views.engine_hook_rule_summary import EngineHookRuleSummaryEndPoint
from dongtai_web.views.engine_hook_rule_type_add import EngineHookRuleTypeAddEndPoint
from dongtai_web.views.engine_hook_rule_type_disable import (
    EngineHookRuleTypeDisableEndPoint,
)
from dongtai_web.views.engine_hook_rule_type_enable import (
    EngineHookRuleTypeEnableEndPoint,
)
from dongtai_web.views.engine_hook_rule_types import EngineHookRuleTypesEndPoint
from dongtai_web.views.engine_hook_rules import EngineHookRulesEndPoint
from dongtai_web.views.engine_method_pool_detail import MethodPoolDetailProxy
from dongtai_web.views.engine_method_pool_search import MethodPoolSearchProxy
from dongtai_web.views.method_graph import MethodGraph
from dongtai_web.views.openapi import OpenApiEndpoint
from dongtai_web.views.profile import (
    ProfileEndpoint,
    ProfileBatchGetEndpoint,
    ProfileBatchModifiedEndpoint,
)
from dongtai_web.views.project_add import ProjectAdd
from dongtai_web.views.project_delete import ProjectDel
from dongtai_web.views.project_detail import ProjectDetail
from dongtai_web.views.project_engines import ProjectEngines
from dongtai_web.views.project_summary import ProjectSummary
from dongtai_web.views.project_search import ProjectSearch
from dongtai_web.views.project_version_add import ProjectVersionAdd
from dongtai_web.views.project_version_current import ProjectVersionCurrent
from dongtai_web.views.project_version_delete import ProjectVersionDelete
from dongtai_web.views.project_version_list import ProjectVersionList
from dongtai_web.views.project_version_update import ProjectVersionUpdate
from dongtai_web.views.projects import Projects


from dongtai_web.views.sca_details import ScaDetailView
from dongtai_web.views.sca_summary import ScaSummary
from dongtai_web.views.scas import ScaList
from dongtai_web.views.strategy_disable import StrategyDisableEndpoint
from dongtai_web.views.strategy_enable import StrategyEnableEndpoint
from dongtai_web.views.strategys import StrategysEndpoint, StrategyEndpoint
from dongtai_web.views.strategys_add import StrategyAdd
from dongtai_web.views.strategys_list import StrategyList
from dongtai_web.views.strategys_type import StrategyType
from dongtai_web.views.strategy_delete import StrategyDelete
from dongtai_web.views.strategy_modified import StrategyModified
from dongtai_web.views.system_info import SystemInfo
from dongtai_web.views.user_detail import UserDetailEndPoint
from dongtai_web.views.user_info import UserInfoEndpoint
from dongtai_web.views.user_login import UserLogin
from dongtai_web.views.user_logout import UserLogout
from dongtai_web.views.user_passwrd import UserPassword
from dongtai_web.views.user_passwrd_reset import UserPasswordReset
from dongtai_web.views.user_register_batch import UserRegisterEndPoint
from dongtai_web.views.user_token import UserToken
from dongtai_web.views.user_token import UserDepartmentToken
from dongtai_web.views.vul_count_for_plugin import VulCountForPluginEndPoint
from dongtai_web.views.vul_delete import VulDelete
from dongtai_web.views.vul_details import (
    VulDetail,
    VulDetailV2,
)
from dongtai_web.views.vul_list_for_plugin import VulListEndPoint
from dongtai_web.views.vul_request_replay import RequestReplayEndPoint
from dongtai_web.views.vul_status import VulStatus
from dongtai_web.views.vul_summary import VulSummary
from dongtai_web.views.vul_summary_type import VulSummaryType
from dongtai_web.views.vul_summary_project import VulSummaryProject
from dongtai_web.views.vuls import VulsEndPoint
from dongtai_web.views.vulnerability_status import VulnerabilityStatusView
from dongtai_web.views.version_update import MethodPoolVersionUpdate
from dongtai_web.views.demo import Demo
from static.i18n.views.setlang import LanguageSetting
from dongtai_web.views.program_language import ProgrammingLanguageList
from dongtai_web.views.filereplace import FileReplace
from dongtai_web.views.messages_list import MessagesEndpoint
from dongtai_web.views.messages_new import MessagesNewEndpoint
from dongtai_web.views.messages_del import MessagesDelEndpoint
from dongtai_web.views.agent_alias_modified import AgentAliasModified
from dongtai_web.views.engine_method_pool_time_range import MethodPoolTimeRangeProxy

from dongtai_web.views.vul_levels import VulLevelList
from dongtai_web.views.sensitive_info_rule import (
    SensitiveInfoRuleViewSet,
    SensitiveInfoPatternTypeView,
    SensitiveInfoPatternValidationView,
    SensitiveInfoRuleBatchView,
    SensitiveInfoRuleAllView,
)
from dongtai_web.views.details_id import (
    AgentListWithid,
    ProjectListWithid,
    ScaListWithid,
    VulsListWithid,
)

from dongtai_web.aggregation.aggregation_del import DelVulMany
from dongtai_web.aggregation.aggregation_project_del import DelVulProjectLevel

from dongtai_web.vul_log.vul_log_view import VulLogViewSet
from dongtai_web.vul_recheck_payload.vul_recheck_payload import VulReCheckPayloadViewSet
from dongtai_web.header_vul.base import HeaderVulViewSet
from dongtai_web.views.new_project_query import NewProjectVersionList
from dongtai_web.enum.hook_rules import HookRuleEnumEndPoint
from django.urls import URLResolver, URLPattern

urlpatterns: list[URLResolver | URLPattern] = [
    path("user/<int:user_id>", UserDetailEndPoint.as_view()),
    path("user/changePassword", UserPassword.as_view()),
    path("user/login", UserLogin.as_view()),
    path("user/logout", UserLogout.as_view()),
    path("user/info", UserInfoEndpoint.as_view()),
    path("user/token", UserToken.as_view()),
    path("user/department/token", UserDepartmentToken.as_view()),
    path("user/password/reset", UserPasswordReset.as_view()),
    path("captcha/", include("captcha.urls")),
    path(r"captcha/refresh", CaptchaCreate.as_view()),
    path("project/<int:id>", ProjectDetail.as_view()),
    path("project/add", ProjectAdd.as_view()),
    path("project/delete", ProjectDel.as_view()),
    path("projects", Projects.as_view()),
    path("projects/summary/<int:id>", ProjectSummary.as_view()),
    path("project/engines/<int:pid>", ProjectEngines.as_view()),
    path("project/search", ProjectSearch.as_view()),
    path("project/version/add", ProjectVersionAdd.as_view()),
    path("project/version/update", ProjectVersionUpdate.as_view()),
    path("project/version/delete", ProjectVersionDelete.as_view()),
    path("project/version/current", ProjectVersionCurrent.as_view()),
    path("project/version/list/<int:project_id>", ProjectVersionList.as_view()),
    path("project/version/check", UpdateProjectVersion.as_view()),
    path("vulns", VulsEndPoint.as_view()),
    path("vuln/summary", VulSummary.as_view()),
    path("vuln/summary_type", VulSummaryType.as_view()),
    path("vuln/summary_project", VulSummaryProject.as_view()),
    path("vuln/<int:id>", VulDetail.as_view()),
    path("vuln/status", VulStatus.as_view()),
    path("vuln/delete/<int:id>", VulDelete.as_view()),
    path("vul/status_list", VulnerabilityStatusView.as_view()),
    path("plugin/vuln/list", VulListEndPoint.as_view()),
    path("plugin/vuln/count", VulCountForPluginEndPoint.as_view()),
    path("scas", ScaList.as_view()),
    path("sca/summary", ScaSummary.as_view()),
    path("sca/<int:id>", ScaDetailView.as_view()),
    path("strategys", StrategysEndpoint.as_view()),
    path("strategy/<int:pk>", StrategyEndpoint.as_view()),
    path("strategy/<int:id>/enable", StrategyEnableEndpoint.as_view()),
    path("strategy/<int:id>/disable", StrategyDisableEndpoint.as_view()),
    path("strategy/<int:id_>/delete", StrategyDelete.as_view()),
    path("strategy/<int:id_>/update", StrategyModified.as_view()),
    path("strategy/types", StrategyType.as_view()),
    path("strategy/user/add", StrategyAdd.as_view()),
    path("strategy/user/list", StrategyList.as_view()),
    path("agent/<int:id_>", Agent.as_view()),
    path("agent/deploy", AgentDeploy.as_view()),
    path("agents", AgentList.as_view()),
    path("agent/<int:pk>/delete", AgentDeleteEndPoint.as_view()),
    path("agents/user", UserAgentList.as_view()),
    path("agent/install", AgentInstall.as_view()),
    path("agent/uninstall", AgentUninstall.as_view()),
    path("agent/status/update", AgentStatusUpdate.as_view()),
    path("agent/start", AgentStart.as_view()),
    path("agent/stop", AgentStop.as_view()),
    path("agents/delete", AgentsDeleteEndPoint.as_view()),
    path("agent/alias/modified", AgentAliasModified.as_view()),
    path("openapi", OpenApiEndpoint.as_view()),
    path("profile/<str:key>", ProfileEndpoint.as_view()),
    path("profile/batch/get", ProfileBatchGetEndpoint.as_view()),
    path("profile/batch/modified", ProfileBatchModifiedEndpoint.as_view()),
    path("system/info", SystemInfo.as_view()),
    path("engine/method_pool/search", MethodPoolSearchProxy.as_view()),
    path("engine/method_pool/detail", MethodPoolDetailProxy.as_view()),
    path("engine/method_pool/timerange", MethodPoolTimeRangeProxy.as_view()),
    path("engine/graph", MethodGraph.as_view()),
    path("engine/request/replay", RequestReplayEndPoint.as_view()),
    path("engine/hook/rule/summary", EngineHookRuleSummaryEndPoint.as_view()),
    path("engine/hook/rule/add", EngineHookRuleAddEndPoint.as_view()),
    path("engine/hook/rule/modify", EngineHookRuleModifyEndPoint.as_view()),
    path("engine/hook/rule/status", EngineHookRuleEnableEndPoint.as_view()),
    path("engine/hook/rule_type/add", EngineHookRuleTypeAddEndPoint.as_view()),
    path("engine/hook/rule_type/disable", EngineHookRuleTypeDisableEndPoint.as_view()),
    path("engine/hook/rule_type/enable", EngineHookRuleTypeEnableEndPoint.as_view()),
    path("engine/hook/rule_types", EngineHookRuleTypesEndPoint.as_view()),
    path("engine/hook/rules", EngineHookRulesEndPoint.as_view()),
    path("documents", DocumentsEndpoint.as_view()),
    path("version_update/K23DiutPrwpoqAddqNbHUk", MethodPoolVersionUpdate.as_view()),
    path("i18n/setlang", LanguageSetting.as_view()),
    path("program_language", ProgrammingLanguageList.as_view()),
    path("filereplace/<str:filename>", FileReplace.as_view()),
    path("message/list", MessagesEndpoint.as_view()),
    path("message/unread_count", MessagesNewEndpoint.as_view()),
    path("message/delete", MessagesDelEndpoint.as_view()),
    path("vul_levels", VulLevelList.as_view()),
    path(
        "sensitive_info_rule",
        SensitiveInfoRuleViewSet.as_view({"get": "list", "post": "create"}),
    ),
    path(
        "sensitive_info_rule/<int:pk>",
        SensitiveInfoRuleViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destory"}
        ),
    ),
    path("sensitive_info_rule/pattern_type", SensitiveInfoPatternTypeView.as_view()),
    path(
        "sensitive_info_rule/<str:pattern_type>_validation",
        SensitiveInfoPatternValidationView.as_view(),
    ),
    path("sensitive_info_rule/batch_update", SensitiveInfoRuleBatchView.as_view()),
    path("sensitive_info_rule/all", SensitiveInfoRuleAllView.as_view()),
    path("agent/list/ids", AgentListWithid.as_view()),
    path("vul/list/ids", VulsListWithid.as_view()),
    path("sca/list/ids", ScaListWithid.as_view()),
    path("project/list/ids", ProjectListWithid.as_view()),
    # get webHook setting
    path("agent/summary/<int:pk>", AgentSummary.as_view()),
    # vul list page of sca and common vul
    path("vul_list_delete", DelVulMany.as_view()),
    path("project_vul_delete", DelVulProjectLevel.as_view()),
    path("vullog/<int:vul_id>", VulLogViewSet.as_view({"get": "list"})),
    path(
        "vul_recheck_payload/<int:pk>",
        VulReCheckPayloadViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "delete"}
        ),
    ),
    path(
        "vul_recheck_payload",
        VulReCheckPayloadViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
    ),
    path(
        "vul_recheck_payload/status",
        VulReCheckPayloadViewSet.as_view(
            {
                "put": "status_change",
            }
        ),
    ),
    path(
        "header_vul",
        HeaderVulViewSet.as_view(
            {
                "get": "list",
            }
        ),
    ),
    path(
        "header_vul/<int:pk>",
        HeaderVulViewSet.as_view(
            {
                "delete": "delete",
            }
        ),
    ),
    path(
        "hook_rule/enum",
        HookRuleEnumEndPoint.as_view(
            {
                "get": "get_enums",
            }
        ),
    ),
]
if os.getenv("environment", None) in ("TEST", "PROD"):
    # demo接口
    urlpatterns.extend(
        [
            path("demo", Demo.as_view()),
            path("user/register", UserRegisterEndPoint.as_view()),
            path("user/register/<str:token>", UserRegisterEndPoint.as_view()),
        ]
    )
if os.getenv("githubcount", None) in ("true",) or os.getenv("environment", None) in (
    "PROD",
):
    from dongtai_web.views.github_contributors import GithubContributorsView

    urlpatterns.extend(
        [
            path("github_contributors", GithubContributorsView.as_view()),
        ]
    )

urlpatterns = [path("api/v1/", include(urlpatterns))]
urlpatterns.extend(
    [
        path("api/v2/vuln/<int:id>", VulDetailV2.as_view()),
        path("api/v2/agents", AgentListv2.as_view({"get": "pagenation_list"})),
        path("api/v2/agents/summary", AgentListv2.as_view({"get": "summary"})),
        path("api/v2/agents/stat", AgentListv2.as_view({"get": "agent_stat"})),
        #  组件漏洞 列表
        path("api/v2/sca_vul_list_content", GetAggregationVulList.as_view()),
        # 组件漏洞 汇总
        path("api/v2/sca_vul_summary", GetScaSummary.as_view()),
        path("api/v2/app_vul_list_content", GetAppVulsList.as_view()),
        path("api/v2/app_vul_summary", GetAppVulsSummary.as_view()),
        path("api/v2/project_version", NewProjectVersionList.as_view()),
    ]
)

# urlpatterns.extend(scaupload_urls) departured
urlpatterns.extend(apitimelog_urls)
urlpatterns.extend(sca_urls)
urlpatterns.extend(versioncontrol_urls)
urlpatterns.extend(systemmonitor_urls)

urlpatterns = format_suffix_patterns(urlpatterns)
