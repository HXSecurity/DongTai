#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/5/21 15:55
# software: PyCharm
# project: webapi
import os
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from iast.account.department import DepartmentEndPoint
from iast.account.talent import TalentEndPoint
from iast.account.user import UserEndPoint
from iast.base.update_project_version import UpdateProjectVersion
from iast.views.agent_delete import AgentDeleteEndPoint
from iast.views.agent_deploy import AgentDeploy
from iast.views.agent_deploy_doc import AgentDeployDesc
from iast.views.agent_deploy_info import AgentDeployInfo
from iast.views.agent_deploy_submit import AgentDeploySave
from iast.views.agent_download import AgentDownload
from iast.views.agent_install import AgentInstall
from iast.views.agent_start import AgentStart
from iast.views.agent_status_update import AgentStatusUpdate
from iast.views.agents_delete import AgentsDeleteEndPoint
from iast.views.agent_stop import AgentStop
from iast.views.agent_uninstall import AgentUninstall
from iast.views.agent_upgrade_offline import AgentUpgradeOffline
from iast.views.agent_upgrade_online import AgentUpgradeOnline
from iast.views.agent import Agent
from iast.views.agent_search import AgentSearch
from iast.views.agents import AgentList
from iast.views.agents_user import UserAgentList
from iast.views.captcha_create import CaptchaCreate
from iast.views.documents import DocumentsEndpoint
from iast.views.engine_hook_rule_add import EngineHookRuleAddEndPoint
from iast.views.engine_hook_rule_modify import EngineHookRuleModifyEndPoint
from iast.views.engine_hook_rule_status import EngineHookRuleEnableEndPoint
from iast.views.engine_hook_rule_summary import EngineHookRuleSummaryEndPoint
from iast.views.engine_hook_rule_type_add import EngineHookRuleTypeAddEndPoint
from iast.views.engine_hook_rule_type_disable import EngineHookRuleTypeDisableEndPoint
from iast.views.engine_hook_rule_type_enable import EngineHookRuleTypeEnableEndPoint
from iast.views.engine_hook_rule_types import EngineHookRuleTypesEndPoint
from iast.views.engine_hook_rules import EngineHookRulesEndPoint
from iast.views.engine_method_pool_detail import MethodPoolDetailProxy
from iast.views.engine_method_pool_sca import EngineMethodPoolSca
from iast.views.engine_method_pool_search import MethodPoolSearchProxy
from iast.views.log_clear import LogClear
from iast.views.log_delete import LogDelete
from iast.views.log_export import LogExport
from iast.views.logs import LogsEndpoint
from iast.views.method_graph import MethodGraph
from iast.views.openapi import OpenApiEndpoint
from iast.views.profile import ProfileEndpoint, ProfileBatchGetEndpoint, ProfileBatchModifiedEndpoint
from iast.views.project_add import ProjectAdd
from iast.views.project_delete import ProjectDel
from iast.views.project_detail import ProjectDetail
from iast.views.project_engines import ProjectEngines
from iast.views.project_report_export import ProjectReportExport
from iast.views.project_summary import ProjectSummary
from iast.views.project_search import ProjectSearch
from iast.views.project_version_add import ProjectVersionAdd
from iast.views.project_version_current import ProjectVersionCurrent
from iast.views.project_version_delete import ProjectVersionDelete
from iast.views.project_version_list import ProjectVersionList
from iast.views.project_version_update import ProjectVersionUpdate
from iast.views.projects import Projects

from iast.views.project_report_sync_add import ProjectReportSyncAdd
from iast.views.project_report_list import ProjectReportList
from iast.views.project_report_download import ProjectReportDownload
from iast.views.project_report_delete import ProjectReportDelete

from iast.views.sca_details import ScaDetailView
from iast.views.sca_sidebar_index import ScaSidebarList
from iast.views.sca_summary import ScaSummary
from iast.views.scas import ScaList
from iast.views.strategy_disable import StrategyDisableEndpoint
from iast.views.strategy_enable import StrategyEnableEndpoint
from iast.views.strategys import StrategysEndpoint, StrategyEndpoint
from iast.views.strategys_add import StrategyAdd
from iast.views.strategys_list import StrategyList
from iast.views.strategys_type import StrategyType
from iast.views.strategy_delete import StrategyDelete
from iast.views.strategy_modified import StrategyModified
from iast.views.system_info import SystemInfo
from iast.views.user_detail import UserDetailEndPoint
from iast.views.user_info import UserInfoEndpoint
from iast.views.user_login import UserLogin
from iast.views.user_logout import UserLogout
from iast.views.user_passwrd import UserPassword
from iast.views.user_passwrd_reset import UserPasswordReset
from iast.views.user_register_batch import UserRegisterEndPoint
from iast.views.user_token import UserToken
from iast.views.vul_count_for_plugin import VulCountForPluginEndPoint
from iast.views.vul_delete import VulDelete
from iast.views.vul_details import VulDetail
from iast.views.vul_list_for_plugin import VulListEndPoint
from iast.views.vul_recheck import VulReCheck
from iast.views.vul_request_replay import RequestReplayEndPoint
from iast.views.vul_sidebar_index import VulSideBarList
from iast.views.vul_status import VulStatus
from iast.views.vul_summary import VulSummary
from iast.views.vul_summary_type import VulSummaryType
from iast.views.vul_summary_project import VulSummaryProject
from iast.views.vuls import VulsEndPoint
from iast.views.vulnerability_status import VulnerabilityStatusView
from iast.views.version_update import MethodPoolVersionUpdate
from iast.views.demo import Demo
from i18n.views.setlang import LanguageSetting
from iast.views.api_route_search import ApiRouteSearch
from iast.views.api_route_related_request import ApiRouteRelationRequest
from iast.views.api_route_cover_rate import ApiRouteCoverRate
from iast.views.health import HealthView
from iast.views.oss_health import OssHealthView
from iast.views.program_language import ProgrammingLanguageList
from iast.views.filereplace import FileReplace
from iast.views.messages_list import MessagesEndpoint
from iast.views.messages_new import MessagesNewEndpoint
from iast.views.messages_del import MessagesDelEndpoint
from iast.views.messages_send import MessagesSendEndpoint
from iast.views.agent_alias_modified import AgentAliasModified
from iast.views.engine_method_pool_time_range import MethodPoolTimeRangeProxy
from iast.views.vul_levels import VulLevelList
from iast.views.sensitive_info_rule import (
    SensitiveInfoRuleViewSet,
    SensitiveInfoPatternTypeView,
    SensitiveInfoPatternValidationView,
    SensitiveInfoRuleBatchView,
    SensitiveInfoRuleAllView,
)
from iast.views.scan_strategys import (
    ScanStrategyViewSet,
    ScanStrategyRelationProject,
    ScanStrategyBatchView,
    ScanStrategyAllView,
)
from iast.views.sca_export import ScaExport

from iast.views.details_id import (AgentListWithid, ProjectListWithid,
                                   ScaListWithid, VulsListWithid)
from iast.views.vul_recheck_v2 import VulReCheckv2


urlpatterns = [
    path("talents", TalentEndPoint.as_view()),
    path("talent/<int:pk>", TalentEndPoint.as_view()),
    path("talent/add", TalentEndPoint.as_view()),
    path("talent/<int:pk>/delete", TalentEndPoint.as_view()),
    path('departments', DepartmentEndPoint.as_view()),
    path('department/<int:pk>', DepartmentEndPoint.as_view()),
    path('department/add', DepartmentEndPoint.as_view()),
    path('department/<int:pk>/delete', DepartmentEndPoint.as_view()),
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
    path('user/password/reset', UserPasswordReset.as_view()),
    path('captcha/', include('captcha.urls')),
    path(r'captcha/refresh', CaptchaCreate.as_view()),
    path('project/<int:id>', ProjectDetail.as_view()),
    path('project/add', ProjectAdd.as_view()),
    path('project/delete', ProjectDel.as_view()),
    path('projects', Projects.as_view()),
    path('projects/summary/<int:id>', ProjectSummary.as_view()),
    path('project/engines/<int:pid>', ProjectEngines.as_view()),
    path('project/report/async_add', ProjectReportSyncAdd.as_view()),
    path('project/report/list', ProjectReportList.as_view()),
    path('project/report/download', ProjectReportDownload.as_view()),
    path('project/report/delete', ProjectReportDelete.as_view()),
    path('project/export', ProjectReportExport.as_view()),
    path('project/search', ProjectSearch.as_view()),
    path('project/version/add', ProjectVersionAdd.as_view()),
    path('project/version/update', ProjectVersionUpdate.as_view()),
    path('project/version/delete', ProjectVersionDelete.as_view()),
    path('project/version/current', ProjectVersionCurrent.as_view()),
    path('project/version/list/<int:project_id>',
         ProjectVersionList.as_view()),
    path('project/version/check', UpdateProjectVersion.as_view()),
    path('vulns', VulsEndPoint.as_view()),
    path('vuln/summary', VulSummary.as_view()),
    path('vuln/summary_type', VulSummaryType.as_view()),
    path('vuln/summary_project', VulSummaryProject.as_view()),
    #    path('vuln/list', VulSideBarList.as_view()), Departured
    path('vuln/<int:id>', VulDetail.as_view()),
    path('vuln/status', VulStatus.as_view()),
    path('vuln/delete/<int:id>', VulDelete.as_view()),
    path('vul/recheck', VulReCheck.as_view()),
    path('vul/status_list', VulnerabilityStatusView.as_view()),
    path('plugin/vuln/list', VulListEndPoint.as_view()),
    path('plugin/vuln/count', VulCountForPluginEndPoint.as_view()),
    path('scas', ScaList.as_view()),
    path('sca/summary', ScaSummary.as_view()),
    #    path('sca/list', ScaSidebarList.as_view()), Departured
    path('sca/<int:id>', ScaDetailView.as_view()),
    path('strategys', StrategysEndpoint.as_view()),
    path('strategy/<int:pk>', StrategyEndpoint.as_view()),
    path('strategy/<int:id>/enable', StrategyEnableEndpoint.as_view()),
    path('strategy/<int:id>/disable', StrategyDisableEndpoint.as_view()),
    path('strategy/<int:id_>/delete', StrategyDelete.as_view()),
    path('strategy/<int:id_>/update', StrategyModified.as_view()),
    path('strategy/types', StrategyType.as_view()),
    path('strategy/user/add', StrategyAdd.as_view()),
    path('strategy/user/list', StrategyList.as_view()),
    path('agent/<int:id_>', Agent.as_view()),
    path('agent/deploy/', AgentDeploy.as_view()),
    #    path('agent/deploy/doc', AgentDeployDesc.as_view()), Departured
    #    path('agent/deploy/info', AgentDeployInfo.as_view()),
    #    path('agent/deploy/submit', AgentDeploySave.as_view()),
    path('agents', AgentList.as_view()),
    path('agent/<int:pk>/delete', AgentDeleteEndPoint.as_view()),
    path('agents/user', UserAgentList.as_view()),
    path('agent/install', AgentInstall.as_view()),
    path('agent/uninstall', AgentUninstall.as_view()),
    #path('agent/upgrade/online', AgentUpgradeOnline.as_view()),
    #    path('agent/upgrade/offline', AgentUpgradeOffline.as_view()),
    path('agent/download', AgentDownload.as_view()),
    path('agent/status/update', AgentStatusUpdate.as_view()),
    path('agent/start', AgentStart.as_view()),
    path('agent/stop', AgentStop.as_view()),
    #    path('agents/search', AgentSearch.as_view()),
    path('agents/delete', AgentsDeleteEndPoint.as_view()),
    path('agent/alias/modified', AgentAliasModified.as_view()),
    path('openapi', OpenApiEndpoint.as_view()),
    path('profile/<str:key>', ProfileEndpoint.as_view()),
    path('profile/batch/get', ProfileBatchGetEndpoint.as_view()),
    path('profile/batch/modified', ProfileBatchModifiedEndpoint.as_view()),
    path('system/info', SystemInfo.as_view()),
    path('logs', LogsEndpoint.as_view()),
    path('log/export', LogExport.as_view()),
    path('log/delete', LogDelete.as_view()),
    path('log/clear', LogClear.as_view()),
    path('engine/method_pool/search', MethodPoolSearchProxy.as_view()),
    path('engine/method_pool/detail', MethodPoolDetailProxy.as_view()),
    path('engine/method_pool/timerange', MethodPoolTimeRangeProxy.as_view()),
    path('engine/method_pool/sca', EngineMethodPoolSca.as_view()),
    path('engine/graph', MethodGraph.as_view()),
    path('engine/request/replay', RequestReplayEndPoint.as_view()),
    path('engine/hook/rule/summary', EngineHookRuleSummaryEndPoint.as_view()),
    path('engine/hook/rule/add', EngineHookRuleAddEndPoint.as_view()),
    path('engine/hook/rule/modify', EngineHookRuleModifyEndPoint.as_view()),
    path('engine/hook/rule/status', EngineHookRuleEnableEndPoint.as_view()),
    path('engine/hook/rule_type/add', EngineHookRuleTypeAddEndPoint.as_view()),
    path('engine/hook/rule_type/disable',
         EngineHookRuleTypeDisableEndPoint.as_view()),
    path('engine/hook/rule_type/enable',
         EngineHookRuleTypeEnableEndPoint.as_view()),
    path('engine/hook/rule_types', EngineHookRuleTypesEndPoint.as_view()),
    path('engine/hook/rules', EngineHookRulesEndPoint.as_view()),
    path('documents', DocumentsEndpoint.as_view()),
    path('version_update/K23DiutPrwpoqAddqNbHUk',
         MethodPoolVersionUpdate.as_view()),
    path('i18n/setlang', LanguageSetting.as_view()),
    path('api_route/search', ApiRouteSearch.as_view()),
    path('api_route/relationrequest', ApiRouteRelationRequest.as_view()),
    path('api_route/cover_rate', ApiRouteCoverRate.as_view()),
    path('health', HealthView.as_view()),
    path('oss/health', OssHealthView.as_view()),
    path('program_language', ProgrammingLanguageList.as_view()),
    path('filereplace/<str:filename>', FileReplace.as_view()),
    path('message/list', MessagesEndpoint.as_view()),
    path('message/unread_count', MessagesNewEndpoint.as_view()),
    path('message/delete', MessagesDelEndpoint.as_view()),
    path('vul_levels', VulLevelList.as_view()),
    #    path('message/send', MessagesSendEndpoint.as_view()),
    path('sensitive_info_rule',
         SensitiveInfoRuleViewSet.as_view({
             'get': 'list',
             'post': 'create'
         })),
    path(
        'sensitive_info_rule/<int:pk>',
        SensitiveInfoRuleViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'delete': 'destory'
        })),
    path('sensitive_info_rule/pattern_type',
         SensitiveInfoPatternTypeView.as_view()),
    path('sensitive_info_rule/<str:pattern_type>_validation',
         SensitiveInfoPatternValidationView.as_view()),
    path('scan_strategy',
         ScanStrategyViewSet.as_view({
             'get': 'list',
             'post': 'create'
         })),
    path(
        'scan_strategy/<int:pk>',
        ScanStrategyViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'delete': 'destory'
        })),
    path('scan_strategy/<int:pk>/relationprojects',
         ScanStrategyRelationProject.as_view()),
    path('sensitive_info_rule/batch_update',
         SensitiveInfoRuleBatchView.as_view()),
    path('sensitive_info_rule/all', SensitiveInfoRuleAllView.as_view()),
    path('scan_strategy/all', ScanStrategyAllView.as_view()),
    path('sca_export', ScaExport.as_view()),
    path('agent/list/ids', AgentListWithid.as_view()),
    path('vul/list/ids', VulsListWithid.as_view()),
    path('sca/list/ids', ScaListWithid.as_view()),
    path('project/list/ids', ProjectListWithid.as_view()),
]
if os.getenv('environment', None) in ('TEST', 'PROD'):
    # demo接口
    urlpatterns.extend([
        path('demo', Demo.as_view()),
        path('user/register', UserRegisterEndPoint.as_view()),
        path('user/register/<str:token>', UserRegisterEndPoint.as_view()),
    ])
if os.getenv('githubcount', None) in ('true', ) or os.getenv('environment', None) in ('PROD',):
    from iast.views.github_contributors import GithubContributorsView
    urlpatterns.extend([
        path('github_contributors', GithubContributorsView.as_view()),
    ])

urlpatterns = [path('api/v1/', include(urlpatterns))]
urlpatterns.extend([path('api/v2/vul/recheck', VulReCheckv2.as_view())])
urlpatterns = format_suffix_patterns(urlpatterns)
