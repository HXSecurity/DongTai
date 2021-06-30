#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/4/30 下午3:00
# project: dongtai-engine
import json
import time

import requests
from django.dispatch import receiver
from dongtai_models.models.notify_config import IastNotifyConfig
from dongtai_models.models.vulnerablity import IastVulnerabilityModel

from signals import vul_found


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
        language: 当前项目所用的语言
        client_ip: 客户端IP
        username: 漏洞所在用户的用户名
    }
    """
    agent = vul.agent
    vul_data = {}
    vul_data['vul_type'] = vul.type
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
    vul_data['language'] = vul.language
    vul_data['client_ip'] = vul.client_ip
    vul_data['username'] = vul.agent.user.get_username()
    return vul_data


@receiver(vul_found)
def save_vul(vul_meta, vul_level, vul_name, vul_stack, top_stack, bottom_stack, **kwargs):
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
        vul.status = '待处理'
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
            status='待处理',
            language=vul_meta.language,
            first_time=vul_meta.create_time,
            latest_time=int(time.time()),
            client_ip=vul_meta.clent_ip,
            param_name=''
        )
        vul.save()

    if vul:
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
        .replace('{{language}}', vul_data['language']) \
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


def send_to_wechat():
    """
    todo 发送漏洞通知到企业微信
    :return:
    """
    pass
