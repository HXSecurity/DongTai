# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/26 下午4:45
# software: PyCharm
# project: lingzhi-engine
from typing import Optional, Any, Union
from dongtai_engine.filters.main import vul_filter
from dongtai_engine.signals.handlers.vul_handler import handler_vul
import hashlib
import json
import time
from json import JSONDecodeError
from itertools import groupby

from celery import shared_task
from celery.apps.worker import logger
from django.db.models import Sum, Q
from django.core.cache import cache
from dongtai_common.engine.vul_engine import VulEngine
from dongtai_common.models import User
from dongtai_common.models.agent_method_pool import MethodPool
from dongtai_common.models.asset import Asset
from dongtai_common.models.errorlog import IastErrorlog
from dongtai_common.models.heartbeat import IastHeartbeat
from dongtai_common.models.replay_method_pool import IastAgentMethodPoolReplay
from dongtai_common.models.replay_queue import IastReplayQueue
from dongtai_common.models.vul_level import IastVulLevel
from dongtai_common.models.vulnerablity import IastVulnerabilityModel
from dongtai_common.utils import const
from dongtai_common.models.agent import IastAgent
from dongtai_common.models.project import IastProject

from dongtai_engine.plugins.strategy_headers import check_response_header
from dongtai_engine.plugins.strategy_sensitive import check_response_content
from dongtai_engine.replay import Replay
from dongtai_conf import settings
from dongtai_web.dongtai_sca.utils import sca_scan_asset
import requests
from dongtai_engine.task_base import replay_payload_data
from dongtai_engine.common.queryset import get_scan_id, load_sink_strategy, get_agent
from dongtai_engine.plugins.project_time_update import project_time_stamp_update
from dongtai_web.vul_log.vul_log import log_recheck_vul

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


def search_and_save_vul(engine: Optional[VulEngine],
                        method_pool_model: Union[IastAgentMethodPoolReplay,
                                                 MethodPool],
                        method_pool: Optional[Any],
                        strategy: dict = {}) -> None:
    """
    搜索方法池是否存在满足策略的数据，如果存在，保存相关数据为漏洞
    :param method_pool_model: 方法池实例化对象
    :param strategy: 策略数据
    :return: None
    """
    logger.info(f'current sink rule is {strategy.get("type")}')
    #queryset = IastStrategyModel.objects.filter(vul_type=strategy['type'],
    #                                            state=const.STRATEGY_ENABLE)
    if not method_pool_model:
        logger.info(
            'method_pool_model missing skip'
        )
        return
    #if not queryset.values('id').exists():
    #    logger.warning(
    #        f'current method pool hit rule {strategy.get("type")}, but no vul strategy.'
    #    )
    #    return
    if method_pool is None:
        method_pool = json.loads(method_pool_model.method_pool
                                 ) if method_pool_model.method_pool else []
    if not method_pool:
        logger.info(
            f'No method_pool in this model id:{method_pool_model.id} , skip')
        return

    engine = VulEngine()
    engine.search(method_pool=method_pool,
                  vul_method_signature=strategy.get('value'))
    status, stack, source_sign, sink_sign, taint_value = engine.result()
    #vul_strategy = queryset.values("level", "vul_name", "id").first()
    #vul_type = queryset.values('vul_type').first()
    #if not vul_strategy or not vul_type:
    #    logger.info(
    #        f'vul data corruption , stop scan in method_pool {method_pool_model.id}'
    #    )
    #    return
    if status:
        filterres = vul_filter(
            stack,
            source_sign,
            sink_sign,
            taint_value,
            strategy['type'],
        )
        logger.info(f'vul filter_status : {filterres}')
    if status and filterres:
        if isinstance(method_pool_model, MethodPool):
            logger.info(f'vul_found {method_pool_model.agent_id}  {method_pool_model.url} {sink_sign}')
        else:
            logger.info(f'vul_found {method_pool_model.id}  {method_pool_model.url} {sink_sign}')
        #vul_strategy = queryset.values("level", "vul_name", "id").first()
        #if not vul_strategy:
        #    pass
        #else:
        handler_vul(
            sender="tasks.search_and_save_vul",
            vul_meta=method_pool_model,
            vul_level=strategy['strategy_level'],
            strategy_id=strategy['strategy_strategy_id'],
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
            vul = IastVulnerabilityModel.objects.filter(id=relation_id).get()
            log_recheck_vul(
                vul.agent.user.id,
                vul.agent.user.username,
                [vul.id],
                '已忽略',
            )
            IastReplayQueue.objects.filter(id=replay_id).update(
                state=const.SOLVED,
                result=const.RECHECK_FALSE,
                verify_time=timestamp,
                update_time=timestamp)
            project_time_stamp_update.apply_async(
                (method_pool_model.agent.bind_project_id, ), countdown=5)
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
        method_pool_model = MethodPool.objects.filter(
            pool_sign=method_pool_sign, agent_id=agent_id).first()
        method_pool_model.agent = get_agent(method_pool_model.agent_id)
        if method_pool_model is None:
            if retryable:
                if self.request.retries < self.max_retries:
                    tries = self.request.retries + 1
                    raise RetryableException(f'漏洞检测方法池 {method_pool_sign} 不存在，重试第 {tries} 次')
                else:
                    logger.warning(f'漏洞检测超过最大重试次数 {self.max_retries}，方法池 {method_pool_sign} 不存在')
            else:
                logger.warning(f'漏洞检测终止，方法池 {method_pool_sign} 不存在')
            return
        logger.info(
            f"search vul from method_pool found,  agent_id: {method_pool_model.agent_id} , uri: {method_pool_model.uri}"
        )
        check_response_header(method_pool_model)
        check_response_content(method_pool_model)
        scan_id = get_scan_id(method_pool_model.agent.bind_project_id)
        strategies = load_sink_strategy(
            scan_id=scan_id)
        engine = VulEngine()
        method_pool = json.loads(method_pool_model.method_pool) if method_pool_model else []
        engine.method_pool = method_pool
        if method_pool:
            # print(engine.method_pool_signatures)
            for strategy in strategies:
                if strategy.get('value') in engine.method_pool_signatures:
                    search_and_save_vul(engine, method_pool_model, None, strategy)
        logger.info(f'漏洞检测完成')
        from dongtai_engine.plugins.method_pool import method_pool_after_scan, enable_method_pool_post_scan_hook
        if method_pool_model and enable_method_pool_post_scan_hook(method_pool_model):
            method_pool_after_scan(method_pool_model)
    except RetryableException as e:
        if self.request.retries < self.max_retries:
            delay = 5 + pow(3, self.request.retries) * 10
            self.retry(exc=e, countdown=delay)
        else:
            logger.info(f'漏洞检测超过最大重试次数，错误原因：{e}')
    except Exception as e:
        logger.error(f'漏洞检测出错，方法池 {method_pool_sign}. 错误原因：{e}', exc_info=e)


@shared_task(queue='dongtai-replay-vul-scan')
def search_vul_from_replay_method_pool(method_pool_id):
    logger.info(f'重放数据漏洞检测开始，方法池 {method_pool_id}')
    try:
        method_pool_model = IastAgentMethodPoolReplay.objects.filter(id=method_pool_id).first()
        if method_pool_model is None:
            logger.warn(f'重放数据漏洞检测终止，方法池 {method_pool_id} 不存在')
            return
        strategies = load_sink_strategy(method_pool_model.agent.user, method_pool_model.agent.language)
        engine = VulEngine()
        method_pool = json.loads(method_pool_model.method_pool) if method_pool_model else []
        engine.method_pool = method_pool
        if method_pool is None or len(method_pool) == 0:
            return
        for strategy in strategies:
            if strategy.get('value') not in engine.method_pool_signatures:
                continue
            search_and_save_vul(engine, method_pool_model, None, strategy)
        logger.info(f'重放数据漏洞检测成功')
    except Exception as e:
        logger.error(f'重放数据漏洞检测出错，方法池 {method_pool_id}. 错误原因：{e}')


#def load_methods_from_strategy(strategy_id):
#    """
#    根据策略ID加载策略详情、策略对应的方法池数据
#    :param strategy_id: 策略ID
#    :return:
#    """
#    strategy = HookStrategy.objects.filter(type__in=HookType.objects.filter(type=4), id=strategy_id).first()
#    if strategy is None:
#        logger.info(f'策略[{strategy_id}]不存在')
#        return None, None
#    strategy_value = {
#        'strategy': strategy,
#        'type': strategy.type.first().value,
#        'value': strategy.value.split('(')[0]
#    }
#    # fixme 后续根据具体需要，获取用户对应的数据
#    if strategy is None:
#        return strategy_value, None
#
#    user = User.objects.filter(id=strategy.created_by).first()
#    if user is None:
#        return strategy_value, None
#
#    agents = IastAgent.objects.filter(user=user)
#    if agents.values('id').exists() is False:
#        return strategy_value, None
#
#    method_pool_queryset = MethodPool.objects.filter(agent__in=agents)
#    return strategy_value, method_pool_queryset
#

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
    sha1_str = hashlib.sha1(raw.encode("utf-8"), usedforsecurity=False).hexdigest()
    return sha1_str


def is_alive(agent_id: int, timestamp: int) -> bool:
    """
    Whether the probe is alive or not, the judgment condition: there is a heartbeat log within 2 minutes
    """
    heartbeat_key = f"heartbeat-{agent_id}"
    return True if cache.get(heartbeat_key) is not None else False

@shared_task(queue='dongtai-periodic-task')
def update_agent_status():
    """
    更新Agent状态
    :return:
    """
    from dongtai_engine.plugins.engine_status_change import after_agent_status_update, before_agent_status_update
    before_agent_status_update()
    logger.info('检测引擎状态更新开始')
    timestamp = int(time.time())
    running_agents_ids = list(
        IastAgent.objects.values("id").filter(online=1).values_list(
            'pk', flat=True).all())
    heartbeat_keys = set(map(lambda x: f"heartbeat-{x}", running_agents_ids))
    exists_keys = set(cache.get_many(heartbeat_keys).keys())
    keys_missing = heartbeat_keys - exists_keys
    stop_agent_ids = list(
        map(lambda x: int(x.replace("heartbeat-", "")), keys_missing))
    IastAgent.objects.filter(id__in=stop_agent_ids).update(
        is_running=0, is_core_running=0, online=0)
    vul_id_qs = IastReplayQueue.objects.filter(
        update_time__lte=timestamp - 60 * 5,
        verify_time__isnull=True,
        replay_type=1).values('relation_id').distinct()
    vuls = IastVulnerabilityModel.objects.filter(
        Q(pk__in=vul_id_qs) & ~Q(status_id__in=(3, 5, 6))
    ).select_related("agent__user")
    for _, vul_list in groupby(vuls, lambda x: x.agent.user_id):
        vul_list = list(vul_list)
        log_recheck_vul(
            vul_list[0].agent.user.id,
            vul_list[0].agent.user.username,
            list(map(lambda x: x.id, vul_list)),
            "验证失败",
        )
    logger.info("update offline agent: %s", stop_agent_ids)
    logger.info('检测引擎状态更新成功')
    after_agent_status_update()

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
                    logger.warning(f'污点数据解析出错，原因：{e}', exc_info=e)
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
                        except BaseException:
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
                            headers = base64.b64encode('\n'.join(header_raw).encode("raw_unicode_escape"))
                        except Exception as e:
                            logger.warning(f'请求头解析失败，漏洞ID: {vulnerability["id"]}', exc_info=e)
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
                            headers = base64.b64encode('\n'.join(header_raw).encode("raw_unicode_escape"))
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
