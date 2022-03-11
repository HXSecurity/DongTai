#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/4/30 下午3:00
# project: dongtai-engine
import json
import time

import requests
from celery.apps.worker import logger
from django.dispatch import receiver
from dongtai.models.project import IastProject, VulValidation
from dongtai.models.replay_queue import IastReplayQueue

from dongtai.models.notify_config import IastNotifyConfig
from dongtai.models.vulnerablity import IastVulnerabilityModel
from dongtai.utils import const

from lingzhi_engine import settings
from signals import vul_found
from dongtai.utils.systemsettings import get_vul_validate


def create_vul_data_from_model(vul):
    """

    :param vul:
    :return:{
        http_url: 漏洞所在url
        http_uri: 漏洞所在uri
        context_path: HTTP请求上下文
        http_method: HTTP请求方法
        http_scheme: HTTP请求协议
        http_protocol: HTTP请求协议
        req_header: HTTP请求头
        req_data: HTTP请求体
        res_header: HTTP响应头
        res_body: HTTP响应体
        vul_type: 漏洞类型
        vul_level: 漏洞等级
        full_stack: 漏洞对应的调用链数据
        top_stack: 漏洞对应污点调用链的链首
        bottom_stack: 漏洞对应污点调用链的链尾
        taint_value: 污点值
        taint_position: 污点所在位置
        agent_token: Agent的token
        project: 所在的项目
        counts: 漏洞出现次数
        client_ip: 客户端IP
        username: 漏洞所在用户的用户名
    }
    """
    agent = vul.agent
    vul_data = {}
    vul_data['vul_type'] = vul.hook_type.name
    vul_data['vul_level'] = vul.level.name_value
    vul_data['http_url'] = vul.url
    vul_data['http_uri'] = vul.uri
    vul_data['http_method'] = vul.http_method
    vul_data['http_scheme'] = vul.http_scheme
    vul_data['http_protocol'] = vul.http_protocol
    vul_data['req_header'] = vul.req_header
    vul_data['req_data'] = vul.req_data
    vul_data['res_header'] = vul.res_header
    vul_data['res_body'] = vul.res_body
    vul_data['full_stack'] = vul.full_stack
    vul_data['top_stack'] = vul.top_stack
    vul_data['bottom_stack'] = vul.bottom_stack
    vul_data['taint_value'] = vul.taint_value
    vul_data['taint_position'] = vul.taint_position
    vul_data['agent_token'] = agent.token
    vul_data['project'] = agent.project_name
    vul_data['context_path'] = vul.context_path
    vul_data['counts'] = vul.counts
    vul_data['client_ip'] = vul.client_ip
    vul_data['username'] = vul.agent.user.get_username()
    return vul_data


def equals(source, target):
    if source == target or source in target or target in source:
        return True


def parse_params(param_values, taint_value):
    """
    从param参数中解析污点的位置
    """
    # 分析是否为json
    #
    param_name = None
    _param_items = param_values.split('&')
    for _param_item in _param_items:
        _params = _param_item.split('=')
        _param_name = _params[0]
        _param_value = '='.join(_params[1:])
        if equals(taint_value, _param_value):
            param_name = _param_name
            break
    return param_name


def parse_body(body, taint_value):
    try:
        post_body = json.loads(body)
        for key, value in post_body.items():
            if equals(taint_value, value):
                return key
    except Exception as e:
        return parse_params(body, taint_value)


def parse_header(req_header, taint_value):
    """
    从header头中解析污点的位置
    """
    import base64
    header_raw = base64.b64decode(req_header).decode('utf-8').split('\n')
    for header in header_raw:
        _header_list = header.split(':')
        _header_name = _header_list[0]
        _header_value = ':'.join(_header_list[1:])
        if equals(taint_value, _header_value):
            return _header_name


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
            if equals(taint_value, cookie_value):
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


def parse_taint_position(source_method, vul_meta, taint_value):
    param_names = dict()
    if 'org.springframework.web.method.support.HandlerMethodArgumentResolver.resolveArgument' == source_method:
        # 检查get参数
        if vul_meta.req_params:
            param_name = parse_params(vul_meta.req_params, taint_value)
            if param_name:
                param_names['GET'] = param_name
                print('污点来自GET参数: ' + param_name)

        # 检查post参数
        if vul_meta.req_data:
            param_name = parse_body(vul_meta.req_data, taint_value)
            if param_name:
                param_names['POST'] = param_name
                print('污点来自POST参数: ' + param_name)

        # 检查header
        if vul_meta.req_header:
            param_name = parse_header(vul_meta.req_header, taint_value)
            if param_name:
                param_names['HEADER'] = param_name
                print('污点来自HEADER头: ' + param_name)

        # 检查path
        if vul_meta.uri:
            param_name = parse_path(vul_meta.uri, taint_value)
            if param_name:
                param_names['PATH'] = taint_value
                print('污点来自URI[' + vul_meta.uri + ']: ' + taint_value)

        # fixme 按照哪种策略对数据进行分析和处理呢？如何识别单点与多点
        return param_names
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

    return param_names


def save_vul(vul_meta, vul_level, strategy_id, vul_stack, top_stack, bottom_stack, **kwargs):
    logger.info(
        f'save vul, strategy id: {strategy_id}, from: {"normal" if "replay_id" not in kwargs else "replay"}, id: {vul_meta.id}')
    # 如果是重放请求，且重放请求类型为漏洞验证，更新漏洞状态为
    taint_value = kwargs['taint_value']
    timestamp = int(time.time())
    param_names = parse_taint_position(source_method=top_stack, vul_meta=vul_meta, taint_value=taint_value)
    if parse_params:
        param_name = json.dumps(param_names)
        taint_position = '/'.join(param_names.keys())
    else:
        param_name = ''
        taint_position = ''

    from dongtai.models.agent import IastAgent
    project_agents = IastAgent.objects.filter(project_version_id=vul_meta.agent.project_version_id)
    # 获取 相同项目版本下的数据
    vul = IastVulnerabilityModel.objects.filter(
        strategy_id=strategy_id,
        uri=vul_meta.uri,
        http_method=vul_meta.http_method,
        agent__in=project_agents,
    ).first()
    IastProject.objects.filter(id=vul_meta.agent.bind_project_id).update(latest_time=timestamp)
    if vul:
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
            'req_header', 'req_params', 'req_data', 'res_header', 'res_body', 'taint_value', 'taint_position',
            'method_pool_id', 'context_path', 'client_ip', 'top_stack', 'bottom_stack', 'full_stack', 'counts',
            'latest_time'
        ])
    else:
        from dongtai.models.hook_type import HookType
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
    return vul


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
        IastReplayQueue.objects.create(
            agent=agent,
            relation_id=vul_id,
            state=const.PENDING,
            count=1,
            create_time=timestamp,
            update_time=timestamp,
            replay_type=const.VUL_REPLAY
        )


def handler_replay_vul(vul_meta, vul_level, strategy_id, vul_stack, top_stack, bottom_stack, **kwargs):
    timestamp = int(time.time())
    vul = IastVulnerabilityModel.objects.filter(id=kwargs['relation_id']).first()
    logger.info(f'handle vul replay, current strategy:{vul.strategy_id}, target hook_type:{strategy_id}')
    if vul and vul.strategy_id == strategy_id:
        vul.status_id = settings.CONFIRMED
        vul.latest_time = timestamp
        vul.save(update_fields=['status_id', 'latest_time'])

        IastProject.objects.filter(id=vul_meta.agent.bind_project_id).update(latest_time=timestamp)

        IastReplayQueue.objects.filter(id=kwargs['replay_id']).update(
            state=const.SOLVED,
            result=const.RECHECK_TRUE,
            verify_time=timestamp,
            update_time=timestamp
        )
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
    try:
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
            vul = save_vul(vul_meta, vul_level, strategy_id, vul_stack, top_stack, bottom_stack, **kwargs)
            create_vul_recheck_task(vul_id=vul.id, agent=vul.agent, timestamp=timestamp)
    except Exception as e:
        vul = save_vul(vul_meta, vul_level, strategy_id, vul_stack, top_stack, bottom_stack, **kwargs)
        create_vul_recheck_task(vul_id=vul.id, agent=vul.agent, timestamp=timestamp)

    if vul:
        send_to_wechat(vul)
        send_vul_notify(vul)


def read_notify_config(user):
    # 从云端读取通知信息
    notify_config_models = IastNotifyConfig.objects.values('notify_type', 'notify_metadata').filter(user=user)
    return (True, notify_config_models) if notify_config_models else (False, None)


def send_vul_notify(vul):
    """
    :param vul_data:
    :return:
    """
    support_notify, notify_configs = read_notify_config(vul.agent.user)
    if support_notify:
        vul_data = create_vul_data_from_model(vul=vul)
        for notify_config in notify_configs:
            notify_type = notify_config.get('notify_type')
            if notify_type == IastNotifyConfig.WEB_HOOK:
                metadata = json.loads(notify_config.get('notify_metadata'))
                send_to_web_hook(vul_data=vul_data, web_hook_url=metadata['url'], template=metadata['template'])
            elif notify_type == IastNotifyConfig.JIRA:
                # todo 补充JIRA的通知
                pass
            elif notify_type == IastNotifyConfig.DING_DING:
                # todo 补充钉钉通知
                pass
            elif notify_type == IastNotifyConfig.EMAIL:
                # todo 补充邮件通知
                pass
            else:
                pass
    

def send_to_web_hook(web_hook_url, template, vul_data):
    """
    发送漏洞通知到webhook
    """
    notify_text = template \
        .replace("{{url}}", vul_data['http_url']) \
        .replace("{{uri}}", vul_data['http_uri']) \
        .replace("{{context_path}}", vul_data['context_path']) \
        .replace("{{http_method}}", vul_data['http_method']) \
        .replace("{{http_scheme}}", vul_data['http_scheme']) \
        .replace("{{http_protocol}}", vul_data['http_protocol']) \
        .replace("{{req_header}}", vul_data['req_header']) \
        .replace("{{vul_type}}", vul_data['vul_type']) \
        .replace("{{vul_level}}", vul_data['vul_level']) \
        .replace("{{full_stack}}", vul_data['full_stack']) \
        .replace("{{top_stack}}", vul_data['top_stack']) \
        .replace("{{bottom_stack}}", vul_data['bottom_stack']) \
        .replace('{{taint_value}}', vul_data['taint_value']) \
        .replace('{{taint_position}}', vul_data['taint_position']) \
        .replace('{{agent_token}}', vul_data['agent_token']) \
        .replace('{{project}}', vul_data['project']) \
        .replace('{{counts}}', str(vul_data['counts'])) \
        .replace('{{client_ip}}', vul_data['client_ip']) \
        .replace('{{username}}', vul_data['username'])

    resp = requests.post(url=web_hook_url, json=json.loads(notify_text))
    if resp.status_code == 200:
        pass


def send_to_dingding():
    """
    todo 发送漏洞通知到钉钉
    :return:
    """
    pass


def send_to_wechat(vul):
    """
    todo 发送漏洞通知到企业微信
    :return:
    """
    wechat = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxx"
    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
    }

    message = {
        "msgtype": "text",
        "text": {
            "content": "IAST漏洞扫描告警通知，请相关同事及时处理！！！\n漏洞类型：{}\n危害等级：{}\n漏洞URL：{}\n业务线名称：{}\n探针agent：{}".format(vul.strategy.vul_type, vul.level.name_value, vul.url, vul.agent.project_name, vul.agent.token),
            "mentioned_list":["@all"],
            "mentioned_mobile_list":["@all"]
        },
    }
    
    resp = requests.post(url=wechat, headers=header, data=json.dumps(message))
    if resp.status_code == 200:
        pass
