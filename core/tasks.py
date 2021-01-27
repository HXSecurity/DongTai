#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/26 下午4:45
# software: PyCharm
# project: lingzhi-engine
import json
import time

from celery import shared_task
from celery.apps.worker import logger

from account.models import User
from core.core import VulEngine
from vuln.models.agent import IastAgent
from vuln.models.agent_method_pool import IastAgentMethodPool
from vuln.models.hook_strategy import HookStrategy
from vuln.models.strategy import IastStrategyModel
from vuln.models.vulnerablity import IastVulnerabilityModel


def queryset_to_iterator(queryset):
    """
    将queryset转换为迭代器，解决使用queryset遍历数据导致的一次性加载至内存带来的内存激增问题
    :param queryset:
    :return:
    """
    page_size = 10
    page = 1
    while True:
        temp_queryset = queryset[(page - 1) * page_size:page * page_size - 1]
        page += 1
        if len(temp_queryset) > 0:
            yield temp_queryset
        else:
            break


def load_sink_strategy(user=None):
    strategies = list()
    strategy_models = HookStrategy.objects.filter(created_by__in=[user.id, 1] if user else [1])
    for sub_queryset in queryset_to_iterator(strategy_models):
        if sub_queryset:
            for strategy in sub_queryset:
                strategies.append({
                    'type': strategy.type.first().value,
                    'value': strategy.value.split('(')[0]
                })
        else:
            break
    return strategies


def save_vul(vul_meta, vul_level, vul_name, vul_stack, top_stack, bottom_stack):
    iast_vuls = IastVulnerabilityModel.objects.filter(
        type=vul_name,  # 指定漏洞类型
        url=vul_meta.url,
        http_method=vul_meta.http_method,
        taint_position='',  # 或许补充相关数据
        agent=vul_meta.agent
    )
    if iast_vuls:
        vul = iast_vuls[0]
        vul.req_header = vul_meta.req_header
        vul.req_params = vul_meta.req_params
        # vul.full_stack = json.dumps(self.app_caller, ensure_ascii=False),
        # vul.top_stack = top_stack,
        # vul.bottom_stack = bottom_stack,
        vul.counts = iast_vuls[0].counts + 1
        vul.latest_time = int(time.time())
        vul.status = 'reported'
        vul.save()
    else:
        vul = IastVulnerabilityModel(
            type=vul_name,
            level=vul_level,
            url=vul_meta.url,
            uri=vul_meta.uri,
            http_method=vul_meta.http_method,
            http_scheme=vul_meta.http_scheme,
            http_protocol=vul_meta.http_protocol,
            req_header=vul_meta.req_header,
            req_params=vul_meta.req_params,
            req_data=vul_meta.req_data,
            res_header=vul_meta.res_header,
            res_body=vul_meta.res_body,
            full_stack=json.dumps(vul_stack, ensure_ascii=False),
            top_stack=top_stack,
            bottom_stack=bottom_stack,
            taint_value='',  # fixme: 污点数据，后续补充
            taint_position='',  # fixme 增加污点位置
            agent=vul_meta.agent,
            context_path=vul_meta.context_path,
            counts=1,
            status='reported',
            language=vul_meta.language,
            first_time=vul_meta.create_time,
            latest_time=int(time.time()),
            client_ip=vul_meta.clent_ip,  # fixme 数据库字段创建错误
            param_name=''
        )
        vul.save()


def search_and_save_vul(engine, method_pool_model, strategy):
    method_pool = json.loads(method_pool_model.method_pool) if method_pool_model else []
    engine.search(
        method_pool=method_pool,
        vul_method_signature=strategy.get('value')
    )
    status, stack, source_sign, sink_sign = engine.result()
    if status:
        vul_strategy = IastStrategyModel.objects.filter(vul_type=strategy['type']).first()
        if vul_strategy:
            save_vul(method_pool_model, vul_strategy.level, vul_strategy.vul_name, stack, source_sign,
                     sink_sign)


@shared_task(queue='vul-scan')
def search_vul_from_method_pool(method_pool_id):
    method_pool_model = IastAgentMethodPool.objects.filter(id=method_pool_id).first()
    if method_pool_model is None:
        logger.info(f'方法池[{method_pool_id}]不存在')
    strategies = load_sink_strategy(method_pool_model.agent.user) if method_pool_model else []
    engine = VulEngine()

    for strategy in strategies:
        search_and_save_vul(engine, method_pool_model, strategy)


@shared_task(queue='vul-scan')
def search_vul_from_strategy(strategy_id):
    strategy = HookStrategy.objects.filter(id=strategy_id).first()
    if strategy is None:
        logger.info(f'策略[{strategy_id}]不存在')
    user = User.objects.filter(id=strategy.created_by).first() if strategy else None
    agents = IastAgent.objects.filter(user=user) if user else None
    method_pool_queryset = IastAgentMethodPool.objects.filter(agent__in=agents if agents else [])
    engine = VulEngine()
    strategy_value = {
        'type': strategy.type.first().value,
        'value': strategy.value.split('(')[0]
    }
    for sub_queryset in queryset_to_iterator(method_pool_queryset):
        if sub_queryset:
            for method_pool in sub_queryset:
                search_and_save_vul(engine, method_pool, strategy_value)
