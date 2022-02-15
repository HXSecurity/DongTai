#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/26 下午4:45
# software: PyCharm
# project: lingzhi-engine
import json
import time
from json import JSONDecodeError

from celery import shared_task
from celery.apps.worker import logger
from django.db.models import Sum
from dongtai.engine.vul_engine import VulEngine
from dongtai.models import User
from dongtai.models.agent import IastAgent
from dongtai.models.agent_method_pool import MethodPool
from dongtai.models.asset import Asset
from dongtai.models.errorlog import IastErrorlog
from dongtai.models.heartbeat import IastHeartbeat
from dongtai.models.hook_strategy import HookStrategy
from dongtai.models.hook_type import HookType
from dongtai.models.project import IastProject
from dongtai.models.replay_method_pool import IastAgentMethodPoolReplay
from dongtai.models.replay_queue import IastReplayQueue
from dongtai.models.sca_maven_artifact import ScaMavenArtifact
from dongtai.models.sca_maven_db import ScaMavenDb
from dongtai.models.sca_vul_db import ScaVulDb
from dongtai.models.strategy import IastStrategyModel
from dongtai.models.vul_level import IastVulLevel
from dongtai.models.vulnerablity import IastVulnerabilityModel
from dongtai.utils import const

from core.plugins.strategy_headers import check_response_header
from core.plugins.strategy_sensitive import check_response_content
from core.replay import Replay
from lingzhi_engine import settings
from signals import vul_found
from core.plugins.export_report import ExportPort
from dongtai.models.project_report import ProjectReport
import requests
from hashlib import sha1

LANGUAGE_MAP = {
    "JAVA": 1,
    "PYTHON": 2,
    "PHP": 3,
    "GO": 4
}


def queryset_to_iterator(queryset):
    """
    将queryset转换为迭代器，解决使用queryset遍历数据导致的一次性加载至内存带来的内存激增问题
    :param queryset:
    :return:
    """
    page_size = 10
    page = 1
    while True:
        temp_queryset = queryset[(page - 1) * page_size:page * page_size]
        page += 1
        if len(temp_queryset) > 0:
            yield temp_queryset
        else:
            break


def load_sink_strategy(user=None, language=None):
    """
    加载用户user有权限方法的策略
    :param user:
    :return:
    """
    strategies = list()
    language_id = 0
    if language and language in LANGUAGE_MAP:
        language_id = LANGUAGE_MAP[language]
    strategy_models = HookStrategy.objects.filter(
        type__in=HookType.objects.filter(type=4,
                                         language_id=language_id) if language_id != 0 else HookType.objects.filter(
            type=4),
        created_by__in=[user.id, 1] if user else [1]
    )
    sub_method_signatures = set()
    for sub_queryset in queryset_to_iterator(strategy_models):
        if sub_queryset is None:
            break
        for strategy in sub_queryset:
            strategy_value = strategy.value
            sub_method_signature = strategy_value[:strategy_value.rfind('(')] if strategy_value.rfind(
                '(') > 0 else strategy_value
            if sub_method_signature in sub_method_signatures:
                continue

            sub_method_signatures.add(sub_method_signature)
            strategies.append({
                'strategy': strategy,
                'type': strategy.type.first().value,
                'value': sub_method_signature
            })
    return strategies


def search_and_save_vul(engine, method_pool_model, method_pool, strategy):
    """
    搜索方法池是否存在满足策略的数据，如果存在，保存相关数据为漏洞
    :param engine: 云端检测引擎
    :param method_pool_model: 方法池实例化对象
    :param strategy: 策略数据
    :return: None
    """
    logger.info(f'current sink rule is {strategy.get("type")}')

    queryset = IastStrategyModel.objects.filter(vul_type=strategy['type'], state=const.STRATEGY_ENABLE)
    if queryset.values('id').exists() is False:
        logger.error(f'current method pool hit rule {strategy.get("type")}, but no vul strategy.')
        return

    engine.search(method_pool=method_pool, vul_method_signature=strategy.get('value'))
    status, stack, source_sign, sink_sign, taint_value = engine.result()

    if status:
        vul_strategy = queryset.values("level", "vul_name", "id").first()
        vul_found.send(
            sender="tasks.search_and_save_vul",
            vul_meta=method_pool_model,
            vul_level=vul_strategy['level'],
            strategy_id=vul_strategy['id'],
            vul_stack=stack,
            top_stack=source_sign,
            bottom_stack=sink_sign,
            taint_value=taint_value
        )
    else:
        try:
            if isinstance(method_pool_model, MethodPool):
                return

            replay_type = method_pool_model.replay_type
            if replay_type != const.VUL_REPLAY:
                return

            replay_id = method_pool_model.replay_id
            relation_id = method_pool_model.relation_id
            timestamp = int(time.time())

            IastVulnerabilityModel.objects.filter(id=relation_id).update(
                status_id=settings.IGNORE,
                latest_time=timestamp
            )
            IastReplayQueue.objects.filter(id=replay_id).update(
                state=const.SOLVED,
                result=const.RECHECK_FALSE,
                verify_time=timestamp,
                update_time=timestamp
            )
            IastProject.objects.filter(id=method_pool.agent.bind_project_id).update(latest_time=timestamp)
        except Exception as e:
            logger.info(f'漏洞数据处理出错，原因：{e}')


def search_and_save_sink(engine, method_pool_model, strategy):
    """
    从方法池中搜索策略strategy对应的sink方法是否存在，如果存在，保存策略与污点池关系
    :param engine: 云端搜索引擎实例化对象
    :param method_pool_model: 方法池模型对象
    :param strategy: json格式的策略
    :return: None
    """
    method_pool = json.loads(method_pool_model.method_pool)
    # fixme 检索匹配条件的sink点
    is_hit = engine.search_sink(
        method_pool=method_pool,
        vul_method_signature=strategy.get('value')
    )
    if is_hit is None:
        return

    logger.info(f'发现sink点{strategy.get("type")}')
    method_pool_model.sinks.add(strategy.get('strategy'))


@shared_task(queue='dongtai-method-pool-scan')
def search_vul_from_method_pool(method_pool_id):
    logger.info(f'漏洞检测开始，方法池 {method_pool_id}')
    try:
        method_pool_model = MethodPool.objects.filter(id=method_pool_id).first()
        if method_pool_model is None:
            logger.warn(f'漏洞检测终止，方法池 {method_pool_id} 不存在')
            return
        check_response_header(method_pool_model)
        check_response_content(method_pool_model)

        strategies = load_sink_strategy(method_pool_model.agent.user, method_pool_model.agent.language)
        engine = VulEngine()

        method_pool = json.loads(method_pool_model.method_pool) if method_pool_model else []
        engine.method_pool = method_pool
        if method_pool:
            for strategy in strategies:
                if strategy.get('value') in engine.method_pool_signatures:
                    search_and_save_vul(engine, method_pool_model, method_pool, strategy)
        logger.info(f'漏洞检测成功')
    except Exception as e:
        logger.error(f'漏洞检测出错，方法池 {method_pool_id}. 错误原因：{e}')


@shared_task(queue='dongtai-replay-vul-scan')
def search_vul_from_replay_method_pool(method_pool_id):
    logger.info(f'重放数据漏洞检测开始，方法池 {method_pool_id}')
    try:
        method_pool_model = IastAgentMethodPoolReplay.objects.filter(id=method_pool_id).first()
        if method_pool_model is None:
            logger.warn(f'重放数据漏洞检测终止，方法池 {method_pool_id} 不存在')
        strategies = load_sink_strategy(method_pool_model.agent.user, method_pool_model.agent.language)
        engine = VulEngine()

        method_pool = json.loads(method_pool_model.method_pool)
        if method_pool is None or len(method_pool) == 0:
            return

        engine.method_pool = method_pool
        for strategy in strategies:
            if strategy.get('value') not in engine.method_pool_signatures:
                continue

            search_and_save_vul(engine, method_pool_model, method_pool, strategy)
        logger.info(f'重放数据漏洞检测成功')
    except Exception as e:
        logger.error(f'重放数据漏洞检测出错，方法池 {method_pool_id}. 错误原因：{e}')


@shared_task(queue='dongtai-strategy-scan')
def search_vul_from_strategy(strategy_id):
    """
    根据sink方法策略ID搜索已有方法池中的数据是否存在满足条件的数据
    :param strategy_id: 策略ID
    :return: None
    """
    logger.info(f'漏洞检测开始，策略 {strategy_id}')
    try:
        strategy_value, method_pool_queryset = load_methods_from_strategy(strategy_id=strategy_id)
        engine = VulEngine()

        for sub_queryset in queryset_to_iterator(method_pool_queryset):
            if sub_queryset:
                for method_pool_model in sub_queryset:
                    method_pool = json.loads(method_pool_model.method_pool) if method_pool_model else []
                    search_and_save_vul(engine, method_pool_model, method_pool, strategy_value)
        logger.info(f'漏洞检测成功')
    except Exception as e:
        logger.error(f'漏洞检测出错，错误原因：{e}')


@shared_task(queue='dongtai-search-scan')
def search_sink_from_method_pool(method_pool_id):
    """
    根据方法池ID搜索方法池中是否匹配到策略库中的sink方法
    :param method_pool_id: 方法池ID
    :return: None
    """
    logger.info(f'sink规则扫描开始，方法池ID[{method_pool_id}]')
    try:
        method_pool_model = MethodPool.objects.filter(id=method_pool_id).first()
        if method_pool_model is None:
            logger.warn(f'sink规则扫描终止，方法池 [{method_pool_id}] 不存在')
            return
        strategies = load_sink_strategy(method_pool_model.agent.user, method_pool_model.agent.language)
        engine = VulEngine()

        for strategy in strategies:
            search_and_save_sink(engine, method_pool_model, strategy)
        logger.info(f'sink规则扫描完成')
    except Exception as e:
        logger.error(f'sink规则扫描出错，错误原因：{e}')


@shared_task(queue='dongtai-search-scan')
def search_sink_from_strategy(strategy_id):
    """
    根据策略ID搜索方法池中是否匹配到当前策略
    :param strategy_id: 策略ID
    :return: None
    """
    logger.info(f'sink规则扫描开始')
    try:
        strategy_value, method_pool_queryset = load_methods_from_strategy(strategy_id=strategy_id)

        engine = VulEngine()
        for sub_queryset in queryset_to_iterator(method_pool_queryset):
            if sub_queryset is None:
                break
            for method_pool in sub_queryset:
                search_and_save_sink(engine, method_pool, strategy_value)
        logger.info(f'sink规则扫描完成')
    except Exception as e:
        logger.error(f'sink规则扫描出错，错误原因：{e}')


def load_methods_from_strategy(strategy_id):
    """
    根据策略ID加载策略详情、策略对应的方法池数据
    :param strategy_id: 策略ID
    :return:
    """
    strategy = HookStrategy.objects.filter(type__in=HookType.objects.filter(type=4), id=strategy_id).first()
    if strategy is None:
        logger.info(f'策略[{strategy_id}]不存在')
        return None, None
    strategy_value = {
        'strategy': strategy,
        'type': strategy.type.first().value,
        'value': strategy.value.split('(')[0]
    }
    # fixme 后续根据具体需要，获取用户对应的数据
    if strategy is None:
        return strategy_value, None

    user = User.objects.filter(id=strategy.created_by).first()
    if user is None:
        return strategy_value, None

    agents = IastAgent.objects.filter(user=user)
    if agents.values('id').exists() is False:
        return strategy_value, None

    method_pool_queryset = MethodPool.objects.filter(agent__in=agents)
    return strategy_value, method_pool_queryset


def get_project_agents(agent):
    agents = IastAgent.objects.filter(
        bind_project_id=agent.bind_project_id,
        project_version_id=agent.project_version_id,
        user=agent.user
    )
    return agents

def sca_scan_asset(asset):

    """
    根据SCA数据库，更新SCA记录信息
    :return:
    """
    search_query = ""
    agent = asset.agent
    version = None
    vul_count = 0
    user_upload_package = None
    if agent.language == "JAVA" and asset.signature_value:
        # 用户上传的组件
        user_upload_package = ScaMavenDb.objects.filter(sha_1=asset.signature_value).first()
        search_query = "hash=" + asset.signature_value

    elif agent.language == "PYTHON":
        # @todo agent上报版本 or 捕获全量pip库
        version = asset.version
        name = asset.package_name.replace("-" + version, "")
        search_query = "ecosystem={}&name={}&version={}".format("PyPI", name, version)

    if search_query == "":
        logger.info(f'search_query empty can not search vuls')
    else:
        package_name = asset.package_name

        try:

            url = settings.SCA_BASE_URL + "/package_vul/?" + search_query
            logger.info(f'sca url: {url}')
            resp = requests.get(url=url)
            resp = json.loads(resp.content)
            maven_model = resp.get("data", {}).get("package", {})
            if maven_model is None:
                maven_model = {}
            vul_list = resp.get("data", {}).get("vul_list", {})

            package_name = maven_model.get('aql', package_name)
            version = maven_model.get('version', version)
            if user_upload_package is not None:
                package_name = user_upload_package.aql
                version = user_upload_package.version

            vul_count = len(vul_list)
            levels = []
            update_fields = list()

            if asset.package_name != package_name:
                asset.package_name = package_name
                update_fields.append('package_name')

            if asset.version != version:
                asset.version = version
                update_fields.append('version')

            for vul in vul_list:
                _level = vul.get("vul_package", {}).get("severity", "none")
                if _level and _level not in levels:
                    levels.append(_level)

            if len(levels) > 0:

                if 'critical' in levels:
                    level = 'high'
                elif 'high' in levels:
                    level = 'high'
                elif 'medium' in levels:
                    level = 'medium'
                elif 'low' in levels:
                    level = 'low'
                else:
                    level = 'info'
            else:
                level = 'info'
            new_level = IastVulLevel.objects.get(name=level)
            if asset.level != new_level:
                asset.level = IastVulLevel.objects.get(name=level)
                update_fields.append('level')

            if asset.vul_count != vul_count:
                asset.vul_count = vul_count
                update_fields.append('vul_count')

            if len(update_fields) > 0:
                logger.info(f'update dependency fields: {update_fields}')
                asset.save(update_fields=update_fields)

        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.info("get package_vul failed:{}".format(e))


@shared_task(queue='dongtai-sca-task')
def update_one_sca(agent_id, package_path, package_signature, package_name, package_algorithm):

    """
    根据SCA数据库，更新SCA记录信息
    :return:
    """
    logger.info(f'SCA检测开始 [{agent_id} {package_path} {package_signature} {package_name} {package_algorithm}]')
    agent = IastAgent.objects.filter(id=agent_id).first()
    version = None
    if agent.language == "JAVA":
        version = package_name.split('/')[-1].replace('.jar', '').split('-')[-1]
    elif agent.language == "PYTHON":
        # @todo agent上报版本 or 捕获全量pip库
        version = package_name.split('/')[-1].split('-')[-1]

    current_version_agents = get_project_agents(agent)
    if package_signature:
        asset_count = Asset.objects.values("id").filter(signature_value=package_signature,
                                                        agent__in=current_version_agents).count()
    else:
        package_signature = sha_1('-'.join([package_name, version]))
        asset_count = Asset.objects.values("id").filter(package_name=package_name,
                                                        version=version,
                                                        agent__in=current_version_agents).count()

    if asset_count == 0:
        new_level = IastVulLevel.objects.get(name="info")
        asset = Asset.objects.create(
            package_name=package_name,
            package_path=package_path,
            signature_algorithm=package_algorithm,
            signature_value=package_signature,
            dt=time.time(),
            version=version,
            level=new_level,
            vul_count=0,
            agent=agent
        )
        sca_scan_asset(asset)
    else:
        logger.info(
            f'SCA检测开始 [{agent_id} {package_path} {package_signature} {package_name} {package_algorithm}] 组件已存在')

@shared_task(queue='dongtai-periodic-task')
def update_all_sca():
    """
    根据SCA数据库，更新SCA记录信息
    :return:
    """
    logger.info(f'SCA离线检测开始')
    try:
        assets = Asset.objects.all()
        if assets.values('id').count() == 0:
            logger.info('dependency is empty')
            return

        step = 20
        start = 0
        while True:
            asset_steps = assets[start:(start + 1) * step]
            if len(asset_steps) == 0:
                break

            for asset in asset_steps:
                sca_scan_asset(asset)
            start = start + 1
        logger.info('SCA离线检测完成')
    except Exception as e:
        logger.error(f'SCA离线检测出错，错误原因：{e}')

def sha_1(raw):
    h = sha1()
    h.update(raw.encode('utf-8'))
    return h.hexdigest()

def is_alive(agent_id, timestamp):
    """
    Whether the probe is alive or not, the judgment condition: there is a heartbeat log within 2 minutes
    """
    return IastHeartbeat.objects.values('id').filter(agent__id=agent_id, dt__gt=(timestamp - 60 * 2)).exists()


@shared_task(queue='dongtai-periodic-task')
def update_agent_status():
    """
    更新Agent状态
    :return:
    """
    logger.info(f'检测引擎状态更新开始')
    timestamp = int(time.time())
    try:
        running_agents = IastAgent.objects.values("id").filter(online=1)
        is_stopped_agents = list()
        for agent in running_agents:
            agent_id = agent['id']
            if is_alive(agent_id=agent_id, timestamp=timestamp):
                continue
            else:
                is_stopped_agents.append(agent_id)
        if is_stopped_agents:
            IastAgent.objects.filter(id__in=is_stopped_agents).update(is_running=0, is_core_running=0, online=0)

        logger.info(f'检测引擎状态更新成功')
    except Exception as e:
        logger.error(f'检测引擎状态更新出错，错误详情：{e}')


@shared_task(queue='dongtai-periodic-task')
def heartbeat():
    """
    发送心跳
    :return:
    """
    # 查询agent数量

    logger.info('core.tasks.heartbeat is running')
    agents = IastAgent.objects.all()
    agent_enable = agents.values('id').filter(is_running=1).count()
    agent_counts = agents.values('id').count()
    heartbeat = IastHeartbeat.objects.values('id').filter(agent__in=agents).annotate(Sum("req_count")).count()
    project_count = IastProject.objects.values('id').count()
    user_count = User.objects.values('id').count()
    vul_count = IastVulnerabilityModel.objects.values('id').count()
    method_pool_count = MethodPool.objects.values('id').count()
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
        logger.info('[core.tasks.heartbeat] send heartbeat data to OpenApi Service.')
        resp = requests.post(url='http://openapi.iast.huoxian.cn:8000/api/v1/engine/heartbeat', json=heartbeat_raw)
        if resp.status_code == 200:
            logger.info('[core.tasks.heartbeat] send heartbeat data to OpenApi Service Successful.')
            pass
        logger.info('[core.tasks.heartbeat] send heartbeat data to OpenApi Service Failure.')
    except Exception as e:
        logger.info(f'[core.tasks.heartbeat] send heartbeat data to OpenApi Service Error. reason is {e}')


@shared_task(queue='dongtai-periodic-task')
def clear_error_log():
    """
    清理错误日志
    :return:
    """
    logger.info(f'日志清理开始')
    try:
        timestamp = int(time.time())
        out_date_timestamp = 60 * 60 * 24 * 30
        count = IastErrorlog.objects.filter(dt__lt=(timestamp - out_date_timestamp)).delete()
        logger.info(f'日志清理成功，共{count}条')
    except Exception as e:
        logger.error(f'日志清理失败，错误详情：{e}')


@shared_task(queue='dongtai-periodic-task')
def export_report():
    """
    导出报告
    :return:
    """
    logger.info(f'导出报告')
    report = ProjectReport.objects.filter(status=0).first()
    if not report:
        logger.info("暂无需要导出的报告")
        return
    try:
        report.status = 1
        report.save()
        export_port = ExportPort()
        export_port.export(report)
    except Exception as e:
        report.status = 0
        report.save()
        logger.error(f'导出报告，错误详情：{e}')


@shared_task(queue='dongtai-replay-task')
def vul_recheck():
    """
    定时处理漏洞验证
    """
    logger.info('开始处理漏洞重放数据')

    relay_queue_queryset = IastReplayQueue.objects.filter(replay_type=const.VUL_REPLAY, state=const.PENDING)
    if relay_queue_queryset is None:
        logger.info('暂无需要处理的漏洞重放数据')
        return

    timestamp = int(time.time())
    sub_replay_queue = relay_queue_queryset[:50]
    for replay in sub_replay_queue:
        # 构造重放请求包
        vul_id = replay.relation_id
        if vul_id is None:
            logger.info('重放请求数据格式不正确，relation id不能为空')
            Replay.replay_failed(timestamp=timestamp, replay=replay)
            continue

        vulnerability = IastVulnerabilityModel.objects.values(
            'id', 'agent', 'uri', 'http_method', 'http_scheme', 'req_header', 'req_params', 'req_data', 'taint_value',
            'param_name'
        ).filter(id=vul_id).first()
        if vulnerability is None:
            Replay.replay_failed(timestamp=timestamp, replay=replay)
            continue

        param_name_value = vulnerability['param_name']
        if param_name_value is not None:
            try:
                params = json.loads(param_name_value)
            except JSONDecodeError as e:
                logger.error(f'污点数据解析出错，原因：{e}')
                Replay.replay_failed(replay=replay, timestamp=timestamp)
                continue

        uri = vulnerability['uri']
        param_value = vulnerability['req_params'] if vulnerability['req_params'] else ''
        headers = vulnerability['req_header']
        body = vulnerability['req_data']
        taint_value = vulnerability['taint_value']

        # 构造带payload的重放请求
        for position, param_name in params.items():
            if position == 'GET':
                _param_items = param_value.split('&')
                item_length = len(_param_items)
                for index in range(item_length):
                    _params = _param_items[index].split('=')
                    _param_name = _params[0]
                    if _param_name == param_name:
                        _param_items[index] = f'{_param_name}=.%2F..%2F%60dongtai'
                        break
                param_value = '&'.join(_param_items)
            elif position == 'POST':
                try:
                    post_body = json.loads(body)
                    if param_name in post_body:
                        post_body[param_name] = '.%2F..%2F%60dongtai'
                        body = json.dumps(post_body)
                    else:
                        _param_items = param_value.split('&')
                        item_length = len(_param_items)
                        for index in range(item_length):
                            _params = _param_items[index].split('=')
                            _param_name = _params[0]
                            if _param_name == param_name:
                                _param_items[index] = f'{_param_name}=.%2F..%2F%60dongtai'
                                break
                        param_value = '&'.join(_param_items)
                except:
                    _param_items = param_value.split('&')
                    item_length = len(_param_items)
                    for index in range(item_length):
                        _params = _param_items[index].split('=')
                        _param_name = _params[0]
                        if _param_name == param_name:
                            _param_items[index] = f'{_param_name}=.%2F..%2F%60dongtai'
                            break
                    param_value = '&'.join(_param_items)
            elif position == 'HEADER':
                import base64
                header_raw = base64.b64decode(headers).decode('utf-8').split('\n')
                item_length = len(header_raw)
                for index in range(item_length):
                    _header_list = header_raw[index].split(':')
                    _header_name = _header_list[0]
                    if _header_name == param_name:
                        header_raw[index] = f'{_header_name}:.%2F..%2F%60dongtai'
                        break
                try:
                    headers = base64.b64encode('\n'.join(header_raw))
                except Exception as e:
                    logger.error(f'请求头解析失败，漏洞ID: {vulnerability["id"]}')
            elif position == 'COOKIE':
                import base64
                header_raw = base64.b64decode(headers).decode('utf-8').split('\n')
                item_length = len(header_raw)
                cookie_index = 0
                cookie_raw = None
                for index in range(item_length):
                    _header_list = header_raw[index].split(':')
                    _header_name = _header_list[0]
                    if _header_name == 'cookie' or _header_name == 'Cookie':
                        cookie_index = index
                        cookie_raw = ':'.join(_header_list[1:])
                        break
                if cookie_index > 0:
                    cookie_raw_items = cookie_raw.split(';')
                    item_length = len(cookie_raw_items)
                    for index in range(item_length):
                        cookie_item = cookie_raw_items[index].split('=')
                        if cookie_item[0] == param_name:
                            cookie_raw_items[index] = f'{param_name}=.%2F..%2F%60dongtai'
                            break
                    cookie_raw = ';'.join(cookie_raw_items)
                    header_raw[cookie_index] = cookie_raw
                try:
                    headers = base64.b64encode('\n'.join(header_raw))
                except Exception as e:
                    logger.error(f'请求头解析失败，漏洞ID: {vulnerability["id"]}')

            elif position == 'PATH':
                # 检查path，替换
                path_items = uri.split('/')
                item_length = len(path_items)
                for index in range(item_length):
                    if taint_value == path_items[index]:
                        path_items[index] = 'dongtai'
                        break
                uri = '/'.join(path_items)

        replay.uri = uri
        replay.method = vulnerability['http_method']
        replay.scheme = vulnerability['http_scheme']
        replay.header = headers
        replay.params = param_value
        replay.body = body
        replay.update_time = timestamp
        replay.state = const.WAITING
        replay.agent_id = vulnerability['agent']
        replay.save(
            update_fields=['uri', 'method', 'scheme', 'header', 'params', 'body', 'update_time', 'state', 'agent_id']
        )

        logger.info('漏洞重放数据处理完成')
