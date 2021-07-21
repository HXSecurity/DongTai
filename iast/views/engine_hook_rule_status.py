#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/2/19 下午3:59
# software: PyCharm
# project: lingzhi-webapi
import logging

from dongtai.endpoint import UserEndPoint, R
from dongtai.models.hook_strategy import HookStrategy
from dongtai.utils import const

logger = logging.getLogger('dongtai-webapi')


class EngineHookRuleEnableEndPoint(UserEndPoint):
    def parse_args(self, request):
        rule_id = request.query_params.get('rule_id')
        rule_type = request.query_params.get('type')
        scope = request.query_params.get('scope')
        op = request.query_params.get('op')
        return rule_id, rule_type, scope, op

    @staticmethod
    def set_strategy_status(strategy_id, strategy_ids, user_id, enable_status):
        if strategy_id:
            rule = HookStrategy.objects.filter(id=strategy_id, created_by=user_id).first()
            if rule:
                rule.enable = enable_status
                rule.save()
                return 1
        elif strategy_ids:
            count = HookStrategy.objects.filter(id__in=strategy_ids, created_by=user_id).update(enable=enable_status)
            return count
        return 0

    @staticmethod
    def check_op(op):
        if op == 'enable':
            op = const.ENABLE
        elif op == 'disable':
            op = const.DISABLE
        elif op == 'delete':
            op = const.DELETE
        else:
            op = None
        return op

    def get(self, request):
        rule_id, rule_type, scope, op = self.parse_args(request)
        user_id = request.user.id
        status = False

        op = self.check_op(op)
        if op is None:
            return R.failure('操作类型不存在')

        if rule_type is not None and scope == 'all':
            count = HookStrategy.objects.filter(type__id=rule_type, created_by=user_id).update(enable=op)
            logger.info('策略类型%s操作成功，共%s条', rule_type, count)
            status = True
        elif rule_id is not None:
            status = self.set_strategy_status(strategy_id=rule_id, strategy_ids=None, user_id=user_id,
                                              enable_status=op)
            logger.info('策略%s操作成功', rule_id)

        if status:
            return R.success(msg='操作成功')
        else:
            return R.failure(msg='策略不存在')

    def post(self, request):
        op = request.data.get('op')
        op = self.check_op(op)
        if op is None:
            return R.failure('操作类型不存在')

        strategy_ids = request.data.get('ids')
        strategy_ids = strategy_ids.split(',')
        if strategy_ids:
            count = self.set_strategy_status(strategy_id=None, strategy_ids=strategy_ids, user_id=request.user.id,
                                             enable_status=op)
            logger.info('策略操作成功，共%s条', count)
            return R.success(msg='操作成功')
        else:
            return R.failure(msg='参数不正确')
