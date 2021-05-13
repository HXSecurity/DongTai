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
from django.db.models import Sum, Q
from dongtai_models.models import User
from dongtai_models.models.agent import IastAgent
from dongtai_models.models.agent_method_pool import MethodPool
from dongtai_models.models.asset import Asset
from dongtai_models.models.heartbeat import Heartbeat
from dongtai_models.models.hook_strategy import HookStrategy
from dongtai_models.models.hook_type import HookType
from dongtai_models.models.project import IastProject
from dongtai_models.models.sca_maven_artifact import ScaMavenArtifact
from dongtai_models.models.sca_vul_db import ScaVulDb
from dongtai_models.models.strategy import IastStrategyModel
from dongtai_models.models.vul_level import IastVulLevel
from dongtai_models.models.vulnerablity import IastVulnerabilityModel

from core.engine import VulEngine
from core.mvn_spider import MavenSpider
from signals import vul_found


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
    """
    加载用户user有权限方法的策略
    :param user:
    :return:
    """
    strategies = list()
    strategy_models = HookStrategy.objects.filter(type__in=HookType.objects.filter(type=4),
                                                  created_by__in=[user.id, 1] if user else [1])
    sub_method_signatures = set()
    for sub_queryset in queryset_to_iterator(strategy_models):
        if sub_queryset:
            for strategy in sub_queryset:
                sub_method_signature = strategy.value.split('(')[0]
                if sub_method_signature not in sub_method_signatures:
                    sub_method_signatures.add(sub_method_signature)
                    strategies.append({
                        'strategy': strategy,
                        'type': strategy.type.first().value,
                        'value': sub_method_signature
                    })
        else:
            break
    return strategies


def save_vul(vul_meta, vul_level, vul_name, vul_stack, top_stack, bottom_stack):
    """
    保存漏洞数据
    :param vul_meta:
    :param vul_level:
    :param vul_name:
    :param vul_stack:
    :param top_stack:
    :param bottom_stack:
    :return:
    """
    vul = IastVulnerabilityModel.objects.filter(
        type=vul_name,  # 指定漏洞类型
        url=vul_meta.url,
        http_method=vul_meta.http_method,
        taint_position='',  # 或许补充相关数据
        agent=vul_meta.agent
    ).first()
    if vul:
        vul.req_header = vul_meta.req_header
        vul.req_params = vul_meta.req_params
        vul.counts = vul.counts + 1
        vul.latest_time = int(time.time())
        vul.status = 'reported'
        vul.full_stack = json.dumps(vul_stack, ensure_ascii=False)
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
            client_ip=vul_meta.clent_ip,
            param_name=''
        )
        vul.save()


def search_and_save_vul(engine, method_pool_model, method_pool, strategy):
    """
    搜索方法池是否存在满足策略的数据，如果存在，保存相关数据为漏洞
    :param engine: 云端检测引擎
    :param method_pool_model: 方法池实例化对象
    :param strategy: 策略数据
    :return: None
    """
    logger.info(f'current sink rule is {strategy.get("type")}')
    vul_strategy = IastStrategyModel.objects.filter(vul_type=strategy['type']).first()
    if vul_strategy:
        engine.search(
            method_pool=method_pool,
            vul_method_signature=strategy.get('value')
        )
        status, stack, source_sign, sink_sign = engine.result()
        if status:
            vul_found.send(sender="tasks.search_and_save_vul", vul_meta=method_pool_model,
                           vul_level=vul_strategy.level,
                           vul_name=vul_strategy.vul_name,
                           vul_stack=stack,
                           top_stack=source_sign,
                           bottom_stack=sink_sign)


def search_and_save_sink(engine, method_pool_model, strategy):
    """
    从方法池中搜索策略strategy对应的sink方法是否存在，如果存在，保存策略与污点池关系
    :param engine: 云端搜索引擎实例化对象
    :param method_pool_model: 方法池模型对象
    :param strategy: json格式的策略
    :return: None
    """
    method_pool = json.loads(method_pool_model.method_pool) if method_pool_model else []
    # fixme 检索匹配条件的sink点
    is_hit = engine.search_sink(
        method_pool=method_pool,
        vul_method_signature=strategy.get('value')
    )
    if is_hit:
        logger.info(f'发现sink点{strategy.get("type")}')
        method_pool_model.sinks.add(strategy.get('strategy'))


@shared_task(queue='vul-scan')
def search_vul_from_method_pool(method_pool_id):
    logger.info('core.tasks.search_vul_from_method_pool is running')
    method_pool_model = MethodPool.objects.filter(id=method_pool_id).first()
    if method_pool_model is None:
        logger.info(f'方法池[{method_pool_id}]不存在')
    strategies = load_sink_strategy(method_pool_model.agent.user)
    engine = VulEngine()

    method_pool = json.loads(method_pool_model.method_pool) if method_pool_model else []
    engine.method_pool = method_pool
    if method_pool:
        for strategy in strategies:
            if strategy.get('value') in engine.method_pool_signatures:
                search_and_save_vul(engine, method_pool_model, method_pool, strategy)
    logger.info('core.tasks.search_sink_from_method_pool is finished')


@shared_task(queue='vul-scan')
def search_vul_from_strategy(strategy_id):
    """
    根据sink方法策略ID搜索已有方法池中的数据是否存在满足条件的数据
    :param strategy_id: 策略ID
    :return: None
    """
    logger.info('core.tasks.search_vul_from_strategy is running')
    strategy_value, method_pool_queryset = load_methods_from_strategy(strategy_id=strategy_id)
    engine = VulEngine()

    for sub_queryset in queryset_to_iterator(method_pool_queryset):
        if sub_queryset:
            for method_pool_model in sub_queryset:
                method_pool = json.loads(method_pool_model.method_pool) if method_pool_model else []
                # todo 对数据做预处理，避免无效的计算
                search_and_save_vul(engine, method_pool_model, method_pool, strategy_value)
    logger.info('core.tasks.search_sink_from_method_pool is finished')


@shared_task(queue='vul-search')
def search_sink_from_method_pool(method_pool_id):
    """
    根据方法池ID搜索方法池中是否匹配到策略库中的sink方法
    :param method_pool_id: 方法池ID
    :return: None
    """
    logger.info('core.tasks.search_sink_from_method_pool is running')
    method_pool_model = MethodPool.objects.filter(id=method_pool_id).first()
    if method_pool_model is None:
        logger.info(f'方法池[{method_pool_id}]不存在')
    strategies = load_sink_strategy(method_pool_model.agent.user)
    engine = VulEngine()

    for strategy in strategies:
        search_and_save_sink(engine, method_pool_model, strategy)
    logger.info('core.tasks.search_sink_from_method_pool is finished')


@shared_task(queue='vul-search')
def search_sink_from_strategy(strategy_id):
    """
    根据策略ID搜索方法池中是否匹配到当前策略
    :param strategy_id: 策略ID
    :return: None
    """
    logger.info('core.tasks.search_sink_from_strategy is running')
    strategy_value, method_pool_queryset = load_methods_from_strategy(strategy_id=strategy_id)

    engine = VulEngine()
    for sub_queryset in queryset_to_iterator(method_pool_queryset):
        if sub_queryset:
            for method_pool in sub_queryset:
                search_and_save_sink(engine, method_pool, strategy_value)
    logger.info('core.tasks.search_sink_from_strategy is finished')


def load_methods_from_strategy(strategy_id):
    """
    根据策略ID加载策略详情、策略对应的方法池数据
    :param strategy_id: 策略ID
    :return:
    """
    strategy = HookStrategy.objects.filter(type__in=HookType.objects.filter(type=4), id=strategy_id).first()
    if strategy is None:
        logger.info(f'策略[{strategy_id}]不存在')
    strategy_value = {
        'strategy': strategy,
        'type': strategy.type.first().value,
        'value': strategy.value.split('(')[0]
    }
    # fixme 后续根据具体需要，获取用户对应的数据
    user = User.objects.filter(id=strategy.created_by).first() if strategy else None
    agents = IastAgent.objects.filter(user=user) if user else None
    method_pool_queryset = MethodPool.objects.filter(agent__in=agents if agents else [])
    return strategy_value, method_pool_queryset


@shared_task(queue='periodic_task')
def update_sca():
    """
    根据SCA数据库，更新SCA记录信息
    :return:
    """
    logger.info('core.tasks.update_sca is running')
    assets = Asset.objects.all()
    for asset in assets:
        signature = asset.signature_value
        aids = ScaMavenArtifact.objects.filter(signature=signature).values("aid")
        vul_count = len(aids)
        levels = ScaVulDb.objects.filter(id__in=aids).values('vul_level')

        level = 'info'
        if len(levels) > 0:
            levels = [_['vul_level'] for _ in levels]
            if 'high' in levels:
                level = 'high'
            elif 'high' in levels:
                level = 'high'
            elif 'medium' in levels:
                level = 'medium'
            elif 'low' in levels:
                level = 'low'
            else:
                level = 'info'
        logger.debug(f'开始更新，sha1: {signature}，危害等级：{level}')
        asset.level = IastVulLevel.objects.get(name=level)
        asset.vul_count = vul_count
        asset.save()
    logger.info('core.tasks.update_sca is finished')


@shared_task(queue='periodic_task')
def update_agent_status():
    """
    更新Agent状态
    :return:
    """
    logger.info('core.tasks.update_agent_status is running')
    timestamp = int(time.time())
    queryset = IastAgent.objects.all()
    no_heart_beat_queryset = queryset.filter((Q(server=None) & Q(latest_time__lt=(timestamp - 600))), is_running=1)
    no_heart_beat_queryset.update(is_running=0)

    heart_beat_queryset = queryset.filter(server__update_time__lt=(timestamp - 600), is_running=1)
    heart_beat_queryset.update(is_running=0)

    logger.info('core.tasks.update_agent_status is finished')


@shared_task(queue='periodic_task')
def heartbeat():
    """
    发送心跳
    :return:
    """
    # 查询agent数量

    logger.info('core.tasks.heartbeat is running')
    agents = IastAgent.objects.all()
    agent_enable = agents.filter(is_running=1).count()
    agent_counts = agents.count()
    heartbeat = Heartbeat.objects.filter(agent__in=agents).annotate(Sum("req_count")).count()
    project_count = IastProject.objects.count()
    user_count = User.objects.count()
    vul_count = IastVulnerabilityModel.objects.count()
    method_pool_count = MethodPool.objects.count()
    heartbeat_raw = {
        "status": 200,
        "msg": "engine is running",
        "agentCount": agent_counts,
        "reqCount": heartbeat,
        "agentEnableCount": agent_enable,
        "projectCount": project_count,
        "userCount": user_count,
        "vulCount": vul_count,
        "methodPoolCount": method_pool_count,
        "timestamp": int(time.time())
    }
    try:
        import requests
        resp = requests.post(url='http://openapi.iast.huoxian.cn:8000/api/v1/engine/heartbeat', json=heartbeat_raw)
        if resp.status_code == 200:
            pass
    except:
        pass


@shared_task(queue='periodic_task')
def maven_spider():
    """
    发送心跳
    :return:
    """
    spider = MavenSpider()
    try:
        spider.cron(MavenSpider.BASEURL, MavenSpider.INDEX)
    except Exception as e:
        logger.error(f'maven爬虫出现异常，异常信息：{e}')


@shared_task(queue='periodic_task')
def clear_error_log():
    """
    清理错误日志
    :return:
    """
    pass
