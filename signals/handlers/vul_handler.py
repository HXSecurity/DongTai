#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/4/30 下午3:00
# project: dongtai-engine
import json
import time

from django.dispatch import receiver

from signals import vul_found
from vuln.models.vulnerablity import IastVulnerabilityModel


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
            client_ip=vul_meta.clent_ip,
            param_name=''
        )
        vul.save()


@receiver(vul_found)
def send_vul_notify(vul_meta, vul_level, vul_name, vul_stack, top_stack, bottom_stack, **kwargs):
    # todo 增加漏洞信息实时通知
    #   1.根据漏洞查找agent
    #   2.根据agent查找用户
    #   3.根据用户查找通知配置
    #   4.根据配置选择webhook、钉钉、企业微信、jira等目标
    #   5.发送通知
    pass


def send_to_web_hook():
    """
    todo 发送漏洞通知到webhook
    """
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
