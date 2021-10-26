#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/10/22 下午2:26
# project: DongTai-engine
import time
from http.client import HTTPResponse
from io import BytesIO

from dongtai.models.hook_type import HookType
from dongtai.models.strategy import IastStrategyModel
from dongtai.models.vulnerablity import IastVulnerabilityModel
from dongtai.utils import const
from celery.apps.worker import logger


class FakeSocket():
    def __init__(self, response_str):
        self._file = BytesIO(response_str)

    def makefile(self, *args, **kwargs):
        return self._file


def parse_response(http_response_str):
    source = FakeSocket(http_response_str.encode())
    response = HTTPResponse(source)
    response.begin()
    return response


def check_csp(response):
    if response.getheader('Content-Security-Policy') is None:
        return True


def check_x_xss_protection(response):
    if response.getheader('X-XSS-Protection') is None:
        return True
    if response.getheader('X-XSS-Protection').strip() == '0':
        return True


def check_strict_transport_security(response):
    if response.getheader('Strict-Transport-Security'):
        # parse max-age
        import re
        result = re.match('max-age=(\d+);.*?', response.getheader('Strict-Transport-Security'))
        if result is None:
            return
        max_age = result.group(1)
        if int(max_age) < 15768000:
            return True


def check_x_frame_options(response):
    if response.getheader('X-Frame-Options') is None:
        return True


def check_x_content_type_options(response):
    if response.getheader('X-Content-Type-Options') is None:
        return True


def check_response_header(method_pool):
    try:
        response = parse_response(method_pool.res_header.strip() + '\n\n' + method_pool.res_body.strip())
        if check_csp(response):
            save_vul('Response Without Content-Security-Policy Header', method_pool)
        if check_x_xss_protection(response):
            save_vul('Response With X-XSS-Protection Disabled', method_pool)
        if check_strict_transport_security(response):
            save_vul('Response With Insecurely Configured Strict-Transport-Security Header', method_pool)
        if check_x_frame_options(response):
            save_vul('Pages Without Anti-Clickjacking Controls', method_pool)
        if check_x_content_type_options(response):
            save_vul('Response Without X-Content-Type-Options Header', method_pool)
    except Exception as e:
        logger.error("check_response_header failed, reason: " + str(e))


def save_vul(vul_type, method_pool):
    hook_type_model = HookType.objects.values('id').filter(
        value=vul_type,
        enable=const.ENABLE,
        created_by__in=(1, method_pool.agent.user.id)
    ).first()
    vul = IastVulnerabilityModel.objects.filter(
        hook_type_id=hook_type_model['id'],
        uri=method_pool.uri,
        http_method=method_pool.http_method,
        method_pool_id=method_pool.id
    ).first()
    timestamp = int(time.time())
    if vul:
        vul.req_header = method_pool.req_header
        vul.req_params = method_pool.req_params
        vul.req_data = method_pool.req_data
        vul.res_header = method_pool.res_header
        vul.res_body = method_pool.res_body
        vul.taint_value = None
        vul.taint_position = None
        vul.context_path = method_pool.context_path
        vul.client_ip = method_pool.clent_ip
        vul.top_stack = None
        vul.bottom_stack = None
        vul.counts = vul.counts + 1
        vul.latest_time = timestamp
        vul.method_pool_id = method_pool.id
        vul.full_stack = None
        vul.status_id = const.VUL_CONFIRMED
        vul.save(update_fields=[
            'req_header', 'req_params', 'req_data', 'res_header', 'res_body', 'taint_value', 'taint_position',
            'method_pool_id', 'context_path', 'client_ip', 'top_stack', 'bottom_stack', 'full_stack', 'counts',
            'latest_time', 'status_id'
        ])
    else:
        vul_strategy = IastStrategyModel.objects.values('level_id').filter(
            hook_type_id=hook_type_model['id'],
            state=const.STRATEGY_ENABLE,
            user_id__in=(1, method_pool.agent.user.id)
        ).first()
        if vul_strategy is None:
            logger.error(f'There is no corresponding strategy for the current vulnerability: {vul_type}')
        IastVulnerabilityModel.objects.create(
            hook_type_id=hook_type_model['id'],
            level_id=vul_strategy['level_id'],
            url=method_pool.url,
            uri=method_pool.uri,
            http_method=method_pool.http_method,
            http_scheme=method_pool.http_scheme,
            http_protocol=method_pool.http_protocol,
            req_header=method_pool.req_header,
            req_params=method_pool.req_params,
            req_data=method_pool.req_data,
            res_header=method_pool.res_header,
            res_body=method_pool.res_body,
            full_stack=None,
            top_stack=None,
            bottom_stack=None,
            taint_value=None,
            taint_position=None,
            agent=method_pool.agent,
            context_path=method_pool.context_path,
            counts=1,
            status_id=const.VUL_CONFIRMED,
            first_time=method_pool.create_time,
            latest_time=timestamp,
            client_ip=method_pool.clent_ip,
            param_name=None,
            method_pool_id=method_pool.id
        )
