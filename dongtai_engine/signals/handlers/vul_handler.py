#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/4/30 下午3:00
# project: dongtai-engine
import json,random
import time
import requests
from celery.apps.worker import logger
from django.dispatch import receiver
from dongtai_common.models.project import IastProject, VulValidation
from dongtai_common.models.replay_queue import IastReplayQueue
from dongtai_common.models.vulnerablity import IastVulnerabilityModel
from dongtai_common.utils import const
from dongtai_conf import settings
from dongtai_engine.signals import vul_found
from dongtai_common.utils.systemsettings import get_vul_validate
from dongtai_web.vul_log.vul_log import log_vul_found, log_recheck_vul
from django.db.models import Q

def equals(source, target):
    if source == target or source in target or target in source:
        return True

from dongtai_engine.signals.handlers.parse_param_name import ParamDict

def parse_params(param_values, taint_value):
    """
    从param参数中解析污点的位置
    """
    from urllib.parse import unquote_plus
    param_name = None
    _param_items = ParamDict(param_values)
    for _param_name, _param_value in _param_items.items():
        if taint_value == _param_value or taint_value == _param_name:
            param_name = _param_name
            break
    for _param_name, _param_value in _param_items.extend_kv_dict.items():
        if taint_value == _param_value or taint_value == _param_name:
            param_name = _param_items.extend_k_map[_param_name]
            break
    _param_items = ParamDict(unquote_plus(param_values))
    for _param_name, _param_value in _param_items.items():
        if taint_value == _param_value or taint_value == _param_name:
            param_name = _param_name
            break
    for _param_name, _param_value in _param_items.extend_kv_dict.items():
        if taint_value == _param_value or taint_value == _param_name:
            param_name = _param_items.extend_k_map[_param_name]
            break
    return param_name


def parse_body(body, taint_value):
    try:
        post_body = json.loads(body)
        for key, value in post_body.items():
            if taint_value == value or taint_value == key:
                return key
    except Exception as e:
        return parse_params(body, taint_value)

from dongtai_engine.filters.utils import parse_headers_dict_from_bytes

def parse_header(req_header, taint_value):
    """
    从header头中解析污点的位置
    """
    import base64
    header_dict = parse_headers_dict_from_bytes(base64.b64decode(req_header))
    for k, v in header_dict.items():
        if v == taint_value or k == taint_value:
            return k



def parse_cookie(req_header, taint_value):
    """
    从cookie中解析
    """
    import base64
    header_raw = base64.b64decode(req_header).decode('utf-8').split('\n')
    cookie_raw = ''
    for header in header_raw:
        # fixme 解析，然后匹配
        _header_list = header.split(':')
        _header_name = _header_list[0]
        if _header_name == 'cookie' or _header_name == 'Cookie':
            cookie_raw = ':'.join(_header_list[1:])
            break

    if cookie_raw:
        cookie_raw_items = cookie_raw.split(';')
        for item in cookie_raw_items:
            cookie_item = item.split('=')
            cookie_value = '='.join(cookie_item[1:])
            if taint_value == cookie_value:
                return cookie_item[0]


def parse_path(uri, taint_value):
    """
    从PathVariable中解析污点位置
    """
    # 根据/拆分uri，然后进行对比
    path_items = uri.split('/')
    for item in path_items:
        if taint_value == item:
            # if equals(taint_value, item):
            # fixme 暂时先使用完全匹配，后续考虑解决误报问题
            return True

from dongtai_engine.signals.handlers.parse_param_name import parse_target_values_from_vul_stack


def parse_taint_position(source_method, vul_meta, taint_value, vul_stack):
    param_names = dict()
    target_values = filter(lambda x: x,
                           parse_target_values_from_vul_stack(vul_stack))
    for taint_value in target_values:
        if 'org.springframework.web.method.support.HandlerMethodArgumentResolver.resolveArgument' == source_method:
            # 检查get参数
            if vul_meta.req_params:
                param_name = parse_params(vul_meta.req_params, taint_value)
                if param_name:
                    param_names['GET'] = param_name
                    logger.info('污点来自GET参数: ' + param_name)

            # 检查post参数
            if vul_meta.req_data:
                param_name = parse_body(vul_meta.req_data, taint_value)
                if param_name:
                    param_names['POST'] = param_name
                    logger.info('污点来自POST参数: ' + param_name)

            # 检查header
            if vul_meta.req_header:
                param_name = parse_header(vul_meta.req_header, taint_value)
                if param_name:
                    param_names['HEADER'] = param_name
                    logger.info('污点来自HEADER头: ' + param_name)

            # 检查path
            if vul_meta.uri:
                param_name = parse_path(vul_meta.uri, taint_value)
                if param_name:
                    param_names['PATH'] = taint_value
                    logger.info('污点来自URI[' + vul_meta.uri + ']: ' + taint_value)

            # fixme 按照哪种策略对数据进行分析和处理呢？如何识别单点与多点
        elif 'javax.servlet.ServletRequest.getParameter' == source_method or 'javax.servlet.ServletRequest.getParameterValues' == source_method:
            if vul_meta.req_params:
                param_name = parse_params(vul_meta.req_params, taint_value)
                if param_name:
                    param_names['GET'] = param_name
            else:
                param_name = parse_params(vul_meta.req_data, taint_value)
                if param_name:
                    param_names['POST'] = param_name
        elif 'javax.servlet.http.HttpServletRequest.getHeader' == source_method:
            # 分析header头
            param_name = parse_header(vul_meta.req_header, taint_value)
            if param_name:
                param_names['HEADER'] = param_name
        elif 'javax.servlet.http.HttpServletRequest.getQueryString' == source_method:
            param_name = parse_params(vul_meta.req_params, taint_value)
            if param_name:
                param_names['GET'] = param_name
        elif 'javax.servlet.http.HttpServletRequest.getCookies' == source_method:
            param_name = parse_cookie(vul_meta.req_header, taint_value)
            if param_name:
                param_names['COOKIE'] = param_name
        else:
            if vul_meta.req_params:
                param_name = parse_params(vul_meta.req_params, taint_value)
                if param_name:
                    param_names['GET'] = param_name
                    logger.info('污点来自GET参数: ' + param_name)

            # 检查post参数
            if vul_meta.req_data:
                param_name = parse_body(vul_meta.req_data, taint_value)
                if param_name:
                    param_names['POST'] = param_name
                    logger.info('污点来自POST参数: ' + param_name)

            # 检查header
            if vul_meta.req_header:
                param_name = parse_header(vul_meta.req_header, taint_value)
                if param_name:
                    param_names['HEADER'] = param_name
                    logger.info('污点来自HEADER头: ' + param_name)

            # 检查path
            if vul_meta.uri:
                param_name = parse_path(vul_meta.uri, taint_value)
                if param_name:
                    param_names['PATH'] = taint_value
                    logger.info('污点来自URI[' + vul_meta.uri + ']: ' + taint_value)

    return param_names

from django.core.cache import cache
import uuid

def save_vul(vul_meta, vul_level, strategy_id, vul_stack, top_stack, bottom_stack, **kwargs):
    logger.info(
        f'save vul, strategy id: {strategy_id}, from: {"normal" if "replay_id" not in kwargs else "replay"}, id: {vul_meta.id}')
    # 如果是重放请求，且重放请求类型为漏洞验证，更新漏洞状态为
    taint_value = kwargs['taint_value']
    timestamp = int(time.time())
    param_names = parse_taint_position(source_method=top_stack, vul_meta=vul_meta, taint_value=taint_value , vul_stack=vul_stack)
    if parse_params:
        param_name = json.dumps(param_names)
        taint_position = '/'.join(param_names.keys())
    else:
        param_name = ''
        taint_position = ''
    logger.info(f"agent_id: {vul_meta.agent_id} vul_uri: {vul_meta.uri} param_name: {param_name}")
    from dongtai_common.models.agent import IastAgent
    project_agents = IastAgent.objects.filter(project_version_id=vul_meta.agent.project_version_id)
    uuid_key = uuid.uuid4().hex
    cache_key = f'vul_save-{strategy_id}-{vul_meta.uri}-{vul_meta.http_method}-{vul_meta.agent.project_version_id}-{param_name}'
    is_api_cached = uuid_key != cache.get_or_set(cache_key, uuid_key)
    if is_api_cached:
        return
    # 获取 相同项目版本下的数据
    vul = IastVulnerabilityModel.objects.filter(
        strategy_id=strategy_id,
        uri=vul_meta.uri,
        http_method=vul_meta.http_method,
        agent__project_version_id=vul_meta.agent.project_version_id,
        param_name=param_name,
    ).order_by('-latest_time').first()
    IastProject.objects.filter(id=vul_meta.agent.bind_project_id).update(latest_time=timestamp)
    if vul:
        vul.url = vul_meta.url
        vul.req_header = vul_meta.req_header
        vul.req_params = vul_meta.req_params
        vul.req_data = vul_meta.req_data
        vul.res_header = vul_meta.res_header
        vul.res_body = vul_meta.res_body
        vul.taint_value = taint_value
        vul.taint_position = taint_position
        vul.context_path = vul_meta.context_path
        vul.client_ip = vul_meta.clent_ip
        vul.top_stack = top_stack
        vul.bottom_stack = bottom_stack
        vul.counts = vul.counts + 1
        vul.latest_time = timestamp
        vul.method_pool_id = vul_meta.id
        vul.full_stack = json.dumps(vul_stack, ensure_ascii=False)
        vul.save(update_fields=[
            'url', 'req_header', 'req_params', 'req_data', 'res_header',
            'res_body', 'taint_value', 'taint_position', 'method_pool_id',
            'context_path', 'client_ip', 'top_stack', 'bottom_stack',
            'full_stack', 'counts', 'latest_time', 'latest_time_desc'
        ])
    else:
        from dongtai_common.models.hook_type import HookType
        hook_type = HookType.objects.filter(vul_strategy_id=strategy_id).first()
        vul = IastVulnerabilityModel.objects.create(
            strategy_id=strategy_id,
            # fixme: delete field hook_type
            hook_type=hook_type if hook_type else HookType.objects.first(),
            level_id=vul_level,
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
            taint_value=taint_value,
            taint_position=taint_position,
            agent=vul_meta.agent,
            context_path=vul_meta.context_path,
            counts=1,
            status_id=settings.PENDING,
            first_time=vul_meta.create_time,
            latest_time=timestamp,
            client_ip=vul_meta.clent_ip,
            param_name=param_name,
            method_pool_id=vul_meta.id
        )
        log_vul_found(vul.agent.user_id, vul.agent.bind_project.name,
                      vul.agent.bind_project_id, vul.id, vul.strategy.vul_name)
    cache.delete(cache_key)
    #delete if exists more than one   departured use redis lock
    #IastVulnerabilityModel.objects.filter(
    #    strategy_id=strategy_id,
    #    uri=vul_meta.uri,
    #    http_method=vul_meta.http_method,
    #    agent__in=project_agents,
    #    param_name=param_name,
    #    pk__lt=vul.id,
    #).delete()

    logger.info(f"vul_found {vul.id}")
    return vul

from dongtai_common.models.vul_recheck_payload import IastVulRecheckPayload

def create_vul_recheck_task(vul_id, agent, timestamp):
    project = IastProject.objects.filter(id=agent.bind_project_id).first()
    if project and project.vul_validation == VulValidation.DISABLE:
        return
    enable_validate = False
    if project is None or (project and project.vul_validation == VulValidation.FOLLOW_GLOBAL):
        enable_validate = get_vul_validate()
    if project and project.vul_validation == VulValidation.ENABLE:
        enable_validate = True

    if enable_validate is False:
        return

    replay_model = IastReplayQueue.objects.filter(replay_type=const.VUL_REPLAY, relation_id=vul_id).first()
    if replay_model:
        if replay_model.state in [const.PENDING, const.WAITING, const.SOLVING]:
            return

        replay_model.state = const.PENDING
        replay_model.update_time = timestamp
        replay_model.count = replay_model.count + 1
        replay_model.save(update_fields=['state', 'update_time', 'count'])
    else:
        vul = IastVulnerabilityModel.objects.filter(
            pk=vul_id).only('strategy_id').first()
        queue = [
            IastReplayQueue(agent=agent,
                            relation_id=vul_id,
                            state=const.PENDING,
                            count=1,
                            create_time=timestamp,
                            update_time=timestamp,
                            replay_type=const.VUL_REPLAY,
                            payload_id=payload_id)
            for payload_id in IastVulRecheckPayload.objects.filter(
                strategy_id=vul.strategy_id,
                user__in=[1, agent.user_id]).values_list('pk', flat=True)
        ]
        if queue:
            IastReplayQueue.objects.bulk_create(queue, ignore_conflicts=True)
        else:
            IastReplayQueue.objects.create(agent=agent,
                                           relation_id=vul_id,
                                           state=const.PENDING,
                                           count=1,
                                           create_time=timestamp,
                                           update_time=timestamp,
                                           replay_type=const.VUL_REPLAY)


def handler_replay_vul(vul_meta, vul_level, strategy_id, vul_stack, top_stack, bottom_stack, **kwargs):
    timestamp = int(time.time())
    vul = IastVulnerabilityModel.objects.filter(id=kwargs['relation_id']).first()
    logger.info(f'handle vul replay, current strategy:{vul.strategy_id}, target hook_type:{strategy_id}')
    if vul and vul.strategy_id == strategy_id:
        vul.status_id = settings.CONFIRMED
        vul.latest_time = timestamp
        vul.save(update_fields=['status_id', 'latest_time','latest_time_desc'])
        IastProject.objects.filter(id=vul_meta.agent.bind_project_id).update(latest_time=timestamp)

        IastReplayQueue.objects.filter(id=kwargs['replay_id']).update(
            state=const.SOLVED,
            result=const.RECHECK_TRUE,
            verify_time=timestamp,
            update_time=timestamp)
        IastReplayQueue.objects.filter(vul_id=vul.id).exclude(
            Q(id=kwargs['replay_id']) | Q(state=const.SOLVED)).update(
                state=const.DISCARD,
                result=const.RECHECK_DISCARD,
                verify_time=timestamp,
                update_time=timestamp)
        log_recheck_vul(vul.agent.user.id, vul.agent.user.username, [vul.id],
                        '已确认')
    else:
        vul = save_vul(vul_meta, vul_level, strategy_id, vul_stack, top_stack, bottom_stack, **kwargs)

        create_vul_recheck_task(vul_id=vul.id, agent=vul.agent, timestamp=timestamp)
    return vul


@receiver(vul_found)
def handler_vul(vul_meta, vul_level, strategy_id, vul_stack, top_stack, bottom_stack, **kwargs):
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
    # 如果是重放请求，且重放请求类型为漏洞验证，更新漏洞状态为
    timestamp = int(time.time())
    from dongtai_common.models.replay_method_pool import IastAgentMethodPoolReplay
    from dongtai_common.models.agent_method_pool import MethodPool

    if isinstance(vul_meta, IastAgentMethodPoolReplay):
        replay_id = vul_meta.replay_id
        replay_type = vul_meta.replay_type
        relation_id = vul_meta.relation_id

        if replay_type == const.VUL_REPLAY:
            kwargs['relation_id'] = relation_id
            kwargs['replay_id'] = replay_id
            vul = handler_replay_vul(vul_meta, vul_level, strategy_id, vul_stack, top_stack, bottom_stack, **kwargs)
        elif replay_type == const.REQUEST_REPLAY:
            # 数据包调试数据暂不检测漏洞
            vul = None
        else:
            vul = save_vul(vul_meta, vul_level, strategy_id, vul_stack,
                           top_stack, bottom_stack, **kwargs)
            create_vul_recheck_task(vul_id=vul.id,
                                    agent=vul.agent,
                                    timestamp=timestamp)
    elif isinstance(vul_meta, MethodPool):
        vul = save_vul(vul_meta, vul_level, strategy_id, vul_stack, top_stack,
                       bottom_stack, **kwargs)
        create_vul_recheck_task(vul_id=vul.id,
                                agent=vul.agent,
                                timestamp=timestamp)
