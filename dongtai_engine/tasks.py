#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/26 下午4:45
# software: PyCharm
# project: lingzhi-engine
import hashlib
import json
import time
from json import JSONDecodeError

from celery import shared_task
from celery.apps.worker import logger
from django.db.models import Sum, Q

from dongtai_common.engine.vul_engine import VulEngine
from dongtai_common.models import User
from dongtai_common.models.agent import IastAgent
from dongtai_common.models.agent_method_pool import MethodPool
from dongtai_common.models.asset import Asset
from dongtai_common.models.errorlog import IastErrorlog
from dongtai_common.models.heartbeat import IastHeartbeat
from dongtai_common.models.hook_strategy import HookStrategy
from dongtai_common.models.hook_type import HookType
from dongtai_common.models.project import IastProject
from dongtai_common.models.replay_method_pool import IastAgentMethodPoolReplay
from dongtai_common.models.replay_queue import IastReplayQueue
from dongtai_common.models.strategy import IastStrategyModel
from dongtai_common.models.vul_level import IastVulLevel
from dongtai_common.models.vulnerablity import IastVulnerabilityModel
from dongtai_common.utils import const

from dongtai_engine.plugins.strategy_headers import check_response_header
from dongtai_engine.plugins.strategy_sensitive import check_response_content
from dongtai_engine.replay import Replay
from dongtai_conf import settings
from dongtai_web.dongtai_sca.utils import sca_scan_asset
from dongtai_common.models.project_report import ProjectReport
import requests
from hashlib import sha1
from dongtai_engine.task_base import replay_payload_data

LANGUAGE_MAP = {
    "JAVA": 1,
    "PYTHON": 2,
    "PHP": 3,
    "GO": 4
}

RETRY_INTERVALS = [10, 30, 90]


class RetryableException(Exception):
    pass


def queryset_to_iterator(queryset):
    """
    将queryset转换为迭代器，解决使用queryset遍历数据导致的一次性加载至内存带来的内存激增问题
    :param queryset:
    :return:
    """
    page_size = 200
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
    :param user: edit by song
    :return:
    """
    logger.info('start load sink_strategy')
    strategies = list()
    language_id = 0
    if language and language in LANGUAGE_MAP:
        language_id = LANGUAGE_MAP[language]
    type_query = HookType.objects.filter(type=4)
    if language_id != 0:
        type_query = type_query.filter(language_id=language_id)

    strategy_models = HookStrategy.objects.filter(
        type__in=type_query,
        created_by__in=[user.id, 1] if user else [1]
    ).values('id', 'value', 'type__value')
    sub_method_signatures = set()
    for strategy in strategy_models:
        # for strategy in sub_queryset:
        strategy_value = strategy.get("value", "")
        sub_method_signature = strategy_value[:strategy_value.rfind('(')] if strategy_value.rfind(
            '(') > 0 else strategy_value
        if sub_method_signature in sub_method_signatures:
            continue
        sub_method_signatures.add(sub_method_signature)

        strategies.append({
            'strategy': strategy.get("id", ""),
            'type': strategy.get("type__value", ""),
            'value': sub_method_signature
        })
    return strategies


from dongtai_engine.signals.handlers.vul_handler import handler_vul
from dongtai_engine.filters.main import vul_filter


def search_and_save_vul(engine, method_pool_model, method_pool, strategy):
    """
    搜索方法池是否存在满足策略的数据，如果存在，保存相关数据为漏洞
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
    filterres = vul_filter(
        stack,
        source_sign,
        sink_sign,
        taint_value,
        queryset.values('vul_type').first()['vul_type'],
        agent_id=method_pool_model.agent_id,
    )
    logger.info(f'vul filter_status : {filterres}')
    if status and filterres:
        logger.info(f'vul_found {method_pool_model.agent_id}  {method_pool_model.url} {sink_sign}')
        vul_strategy = queryset.values("level", "vul_name", "id").first()
        handler_vul(
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


@shared_task(bind=True, queue='dongtai-method-pool-scan',
             max_retries=settings.config.getint('task', 'max_retries', fallback=3))
def search_vul_from_method_pool(self, method_pool_sign, agent_id, retryable=False):
    logger.info(f'漏洞检测开始，方法池 {method_pool_sign}')
    try:
        method_pool_model = MethodPool.objects.filter(pool_sign=method_pool_sign, agent_id=agent_id).first()
        if method_pool_model is None:
            if retryable:
                if self.request.retries < self.max_retries:
                    tries = self.request.retries + 1
                    raise RetryableException(f'漏洞检测方法池 {method_pool_sign} 不存在，重试第 {tries} 次')
                else:
                    logger.error(f'漏洞检测超过最大重试次数 {self.max_retries}，方法池 {method_pool_sign} 不存在')
            else:
                logger.warning(f'漏洞检测终止，方法池 {method_pool_sign} 不存在')
            return
        logger.info(
            f"search vul from method_pool found,  agent_id: {method_pool_model.agent_id} , uri: {method_pool_model.uri}"
        )
        check_response_header(method_pool_model)
        check_response_content(method_pool_model)

        strategies = load_sink_strategy(method_pool_model.agent.user, method_pool_model.agent.language)
        engine = VulEngine()
        method_pool = json.loads(method_pool_model.method_pool) if method_pool_model else []
        engine.method_pool = method_pool
        if method_pool:
            # print(engine.method_pool_signatures)
            for strategy in strategies:
                if strategy.get('value') in engine.method_pool_signatures:
                    search_and_save_vul(engine, method_pool_model, method_pool, strategy)
        logger.info(f'漏洞检测成功')
    except RetryableException as e:
        if self.request.retries < self.max_retries:
            delay = 5 + pow(3, self.request.retries) * 10
            self.retry(exc=e, countdown=delay)
        else:
            logger.error(f'漏洞检测超过最大重试次数，错误原因：{e}')
    except Exception as e:
        logger.error(e, exc_info=True)
        logger.error(f'漏洞检测出错，方法池 {method_pool_sign}. 错误原因：{e}')


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


@shared_task(queue='dongtai-sca-task')
def update_one_sca(agent_id, package_path, package_signature, package_name, package_algorithm, package_version=''):
    """
    根据SCA数据库，更新SCA记录信息
    :return:
    """
    logger.info(
        f'SCA检测开始 [{agent_id} {package_path} {package_signature} {package_name} {package_algorithm} {package_version}]')
    agent = IastAgent.objects.filter(id=agent_id).first()
    version = package_version
    if not version:
        if agent.language == "JAVA":
            version = package_name.split('/')[-1].replace('.jar', '').split('-')[-1]

    if version:
        current_version_agents = get_project_agents(agent)
        if package_signature:
            asset_count = Asset.objects.values("id").filter(signature_value=package_signature,
                                                            agent__in=current_version_agents).count()
        else:
            package_signature = sha_1(package_name)
            asset_count = Asset.objects.values("id").filter(package_name=package_name,
                                                            version=version,
                                                            agent__in=current_version_agents).count()

        if asset_count == 0:
            new_level = IastVulLevel.objects.get(name="info")
            asset = Asset()
            asset.package_name = package_name
            asset.package_path = package_path
            asset.signature_value = package_signature
            asset.signature_algorithm = package_algorithm
            asset.version = version
            asset.level_id = new_level.id
            asset.vul_count = 0
            asset.language = asset.language
            if agent:
                asset.agent = agent
                asset.project_version_id = agent.project_version_id if agent.project_version_id else 0
                asset.project_name = agent.project_name
                asset.language = agent.language
                asset.project_id = -1
                if agent.bind_project_id:
                    asset.project_id = agent.bind_project_id
                asset.user_id = -1
                if agent.user_id:
                    asset.user_id = agent.user_id

            asset.license = ''
            asset.dt = int(time.time())
            asset.save()
            sca_scan_asset(asset)
        else:
            logger.info(
                f'SCA检测开始 [{agent_id} {package_path} {package_signature} {package_name} {package_algorithm} {version}] 组件已存在')


def sha_1(raw):
    sha1_str = hashlib.sha1(raw.encode("utf-8")).hexdigest()
    return sha1_str


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

    logger.info('dongtai_engine.tasks.heartbeat is running')
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
        logger.info('[dongtai_engine.tasks.heartbeat] send heartbeat data to OpenApi Service.')
        resp = requests.post(url='http://openapi.iast.huoxian.cn:8000/api/v1/engine/heartbeat', json=heartbeat_raw)
        if resp.status_code == 200:
            logger.info('[dongtai_engine.tasks.heartbeat] send heartbeat data to OpenApi Service Successful.')
            pass
        logger.info('[dongtai_engine.tasks.heartbeat] send heartbeat data to OpenApi Service Failure.')
    except Exception as e:
        logger.info(f'[dongtai_engine.tasks.heartbeat] send heartbeat data to OpenApi Service Error. reason is {e}')


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
def vul_recheck():
    """
    定时处理漏洞验证
    """
    logger.info('开始处理漏洞重放数据')

    relay_queue_queryset = IastReplayQueue.objects.filter(replay_type=const.VUL_REPLAY, state=const.PENDING).order_by(
        "-id")
    if relay_queue_queryset is None:
        logger.info('暂无需要处理的漏洞重放数据')
        return

    timestamp = int(time.time())
    sub_replay_queue = relay_queue_queryset[:100]
    vul_ids = []
    pool_ids = []
    for item in sub_replay_queue:
        if item.relation_id is None:
            logger.info('重放请求数据格式不正确，relation id不能为空')
            Replay.replay_failed(timestamp=timestamp, replay=item)
            continue
        # 漏洞重放
        if item.replay_type == 1:
            vul_ids.append(item.relation_id)
        # 流量重放
        elif item.replay_type == 2:
            pool_ids.append(item.relation_id)
    if not vul_ids and not pool_ids:
        logger.info('暂无需要处理的漏洞重放数据')
        return
    vul_data = replay_payload_data(vul_ids, 1)
    pool_data = replay_payload_data(pool_ids, 2)
    # print(vul_ids)
    # print(pool_ids)
    for replay in sub_replay_queue:
        # 构造重放请求包
        vul_id = replay.relation_id
        recheck_payload = replay.payload.value if replay.payload_id != -1 else '.%2F..%2F%60dongtai'
        logger.info(
            f"generating payload recheck_payload:{recheck_payload}  vul_id:{vul_id} replay_id:{replay.id}"
        )
        if replay.replay_type == 1:
            vulnerability = vul_data.get(vul_id, {})
        else:
            vulnerability = pool_data.get(vul_id, {})
        if not vulnerability:
            Replay.replay_failed(timestamp=timestamp, replay=replay)
            continue
        uri = vulnerability['uri']
        param_value = vulnerability['req_params'] if vulnerability['req_params'] else ''
        headers = vulnerability['req_header']
        body = vulnerability['req_data']
        logger.info(
            f"generating payload by param_name : {vulnerability['param_name']}"
        )
        if replay.replay_type == 1:
            # 漏洞重放 sink点追加参数
            con = 2
            if vulnerability.get("param_name", ""):
                try:
                    params = json.loads(vulnerability['param_name'])
                except JSONDecodeError as e:
                    logger.error(f'污点数据解析出错，原因：{e}')
                    Replay.replay_failed(replay=replay, timestamp=timestamp)
                    con = 1
            else:
                con = 1
            taint_value = vulnerability['taint_value']
            # 构造带payload的重放请求
            if con == 2:
                for position, param_name in params.items():
                    if position == 'GET':
                        _param_items = param_value.split('&')
                        item_length = len(_param_items)
                        for index in range(item_length):
                            _params = _param_items[index].split('=')
                            _param_name = _params[0]
                            if _param_name == param_name:
                                _param_items[index] = f'{_param_name}={recheck_payload}'
                                break
                        param_value = '&'.join(_param_items)
                    elif position == 'POST':
                        try:
                            # Content-Type: application/json
                            post_body = json.loads(body)
                            if param_name in post_body:
                                post_body[param_name] = recheck_payload
                                body = json.dumps(post_body)
                            else:  # ? it looks weird
                                _param_items = body.split('&')
                                item_length = len(_param_items)
                                for index in range(item_length):
                                    _params = _param_items[index].split('=')
                                    _param_name = _params[0]
                                    if _param_name == param_name:
                                        _param_items[index] = f'{_param_name}={recheck_payload}'
                                        break
                                body = '&'.join(_param_items)
                        except:
                            # Content-Type: multipart/form-data
                            _param_items = body.split('&')
                            item_length = len(_param_items)
                            for index in range(item_length):
                                _params = _param_items[index].split('=')
                                _param_name = _params[0]
                                if _param_name == param_name:
                                    _param_items[index] = f'{_param_name}={recheck_payload}'
                                    break
                            body = '&'.join(_param_items)
                    elif position == 'HEADER':
                        import base64
                        header_raw = base64.b64decode(headers).decode('utf-8').split('\n')
                        item_length = len(header_raw)
                        for index in range(item_length):
                            _header_list = header_raw[index].split(':')
                            _header_name = _header_list[0]
                            if _header_name == param_name:
                                header_raw[index] = f'{_header_name}:{recheck_payload}'
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
                                    cookie_raw_items[index] = f'{param_name}={recheck_payload}'
                                    break
                            cookie_raw = ';'.join(cookie_raw_items)
                            header_raw[cookie_index] = cookie_raw
                        try:
                            headers = base64.b64encode('\n'.join(header_raw))
                        except Exception as e:
                            logger.error(f'请求头解析失败，漏洞ID: {vulnerability["id"]}')

                    elif position == 'PATH' and taint_value:
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
        # print(replay.id)
        # print("okkkkkto======update")
        replay.save(
            update_fields=['uri', 'method', 'scheme', 'header', 'params', 'body', 'update_time', 'state', 'agent_id']
        )

    # IastReplayQueue.objects.bulk_update(relay_queue_queryset, ['uri', 'method', 'scheme', 'header', 'params', 'body', 'update_time', 'state', 'agent_id'])
    logger.info('漏洞重放数据处理完成')
