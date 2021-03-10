#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/25 下午7:01
# software: PyCharm
# project: lingzhi-engine

from django.urls import path

from vuln.views.hook_rule_add import HookRuleAddEndPoint
from vuln.views.hook_rule_delete import HookRuleDeleteEndPoint
from vuln.views.hook_rule_disable import HookRuleDisableEndPoint
from vuln.views.hook_rule_enable import HookRuleEnableEndPoint
from vuln.views.hook_rule_modify import HookRuleModifyEndPoint
from vuln.views.hook_rule_summary import HookRuleSummaryEndPoint
from vuln.views.hook_rule_type_add import HookRuleTypeAddEndPoint
from vuln.views.hook_rule_type_disable import HookRuleTypeDisableEndPoint
from vuln.views.hook_rule_type_enable import HookRuleTypeEnableEndPoint
from vuln.views.hook_rule_types import HookRuleTypesEndPoint
from vuln.views.hook_rules import HookRulesEndPoint
from vuln.views.method_pool import MethodPoolEndPoint
from vuln.views.method_pool_detail import MethodPoolDetailEndPoint
from vuln.views.search import SearchEndPoint
from vuln.views.signer import RunSigner
from vuln.views.strategy_run import StrategyRunEndPoint
from vuln.views.vul_rule import VulRuleEndPoint
from vuln.views.vul_rule_detail import VulRuleDetailEndPoint
from vuln.views.vul_rule_save import VulRuleSaveEndPoint
from vuln.views.vul_rule_type import VulRuleTypeEndPoint

urlpatterns = [
    # todo HTTP数据包调试
    path('search', SearchEndPoint.as_view()),
    path('rule', VulRuleEndPoint.as_view()),
    path('rule/type', VulRuleTypeEndPoint.as_view()),
    path('rule/detail', VulRuleDetailEndPoint.as_view()),
    path('rule/save', VulRuleSaveEndPoint.as_view()),
    path('method_pool/detail', MethodPoolDetailEndPoint.as_view()),
    path('run', StrategyRunEndPoint.as_view()),
    path('method_pools', MethodPoolEndPoint.as_view()),
    path('sign', RunSigner.as_view()),

    # hook rule
    path('hook/rule/summary', HookRuleSummaryEndPoint.as_view()),
    path('hook/rules', HookRulesEndPoint.as_view()),
    path('hook/rule/enable', HookRuleEnableEndPoint.as_view()),
    path('hook/rule/disable', HookRuleDisableEndPoint.as_view()),
    path('hook/rule/delete', HookRuleDeleteEndPoint.as_view()),
    path('hook/rule/add', HookRuleAddEndPoint.as_view()),
    path('hook/rule/modify', HookRuleModifyEndPoint.as_view()),
    path('hook/rule_type/add', HookRuleTypeAddEndPoint.as_view()),
    path('hook/rule_type/enable', HookRuleTypeEnableEndPoint.as_view()),
    path('hook/rule_type/disable', HookRuleTypeDisableEndPoint.as_view()),
    path('hook/rule_types', HookRuleTypesEndPoint.as_view()),

]
