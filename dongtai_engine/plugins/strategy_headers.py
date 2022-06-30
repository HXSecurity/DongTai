#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/10/22 下午2:26
# project: DongTai-engine
import random
import time
from http.client import HTTPResponse
from io import BytesIO

from celery.apps.worker import logger
from django.db.models import Q
from dongtai_common.models.project import IastProject
from dongtai_common.models.strategy import IastStrategyModel
from dongtai_common.models.vulnerablity import IastVulnerabilityModel
from dongtai_common.utils import const

from dongtai_engine.plugins import is_strategy_enable
from dongtai_web.vul_log.vul_log import log_vul_found, log_recheck_vul

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
            save_vul('Response Without Content-Security-Policy Header', method_pool, position='HTTP Response Header')
        if check_x_xss_protection(response):
            save_vul('Response With X-XSS-Protection Disabled', method_pool)
        if check_strict_transport_security(response):
            save_vul('Response With Insecurely Configured Strict-Transport-Security Header', method_pool,
                     position='HTTP Response Header')
        if check_x_frame_options(response):
            save_vul('Pages Without Anti-Clickjacking Controls', method_pool, position='HTTP Response Header')
        if check_x_content_type_options(response):
            save_vul('Response Without X-Content-Type-Options Header', method_pool, position='HTTP Response Header')
    except Exception as e:
        logger.error("check_response_header failed, reason: " + str(e))

from django.core.cache import cache
import uuid

def save_vul(vul_type, method_pool, position=None, data=None):
    if is_strategy_enable(vul_type, method_pool) is False:
        return None
    vul_strategy = IastStrategyModel.objects.filter(
        vul_type=vul_type,
        state=const.STRATEGY_ENABLE,
        user_id__in=(1, method_pool.agent.user.id)
    ).first()
    if vul_strategy is None:
        logger.error(f'There is no corresponding strategy for the current vulnerability: {vul_type}')

    from dongtai_common.models.agent import IastAgent
    project_agents = IastAgent.objects.filter(
        project_version_id=method_pool.agent.project_version_id)
    uuid_key = uuid.uuid4().hex
    cache_key = f'vul_save-{vul_strategy.id}-{method_pool.uri}-{method_pool.http_method}-{method_pool.agent.project_version_id}'
    is_api_cached = uuid_key != cache.get_or_set(cache_key, uuid_key)
    if is_api_cached:
        return
    vul = IastVulnerabilityModel.objects.filter(
        strategy_id=vul_strategy.id,
        uri=method_pool.uri,
        http_method=method_pool.http_method,
        agent__project_version_id=method_pool.agent.project_version_id,
    ).order_by('-latest_time').first()
    timestamp = int(time.time())
    IastProject.objects.filter(id=method_pool.agent.bind_project_id).update(latest_time=timestamp)
    if vul:
        vul.url = vul.url
        vul.req_header = method_pool.req_header
        vul.req_params = method_pool.req_params
        vul.req_data = method_pool.req_data
        vul.res_header = method_pool.res_header
        vul.res_body = method_pool.res_body
        vul.taint_value = data
        vul.taint_position = position
        vul.context_path = method_pool.context_path
        vul.client_ip = method_pool.clent_ip
        vul.counts = vul.counts + 1
        vul.latest_time = timestamp
        vul.method_pool_id = method_pool.id
        vul.save(update_fields=[
            'url', 'req_header', 'req_params', 'req_data', 'res_header',
            'res_body', 'taint_value', 'taint_position', 'context_path',
            'client_ip', 'counts', 'latest_time', 'method_pool_id',
            'latest_time_desc'
        ])
    else:
        from dongtai_common.models.hook_type import HookType
        hook_type = HookType.objects.filter(vul_strategy_id=vul_strategy.id).first()
        vul = IastVulnerabilityModel.objects.create(
            strategy=vul_strategy,
            # fixme: remove field
            hook_type=hook_type if hook_type else HookType.objects.first(),
            level=vul_strategy.level,
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
            taint_value=data,
            taint_position=position,
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
        log_vul_found(vul.agent.user_id, vul.agent.bind_project.name,
                      vul.agent.bind_project_id, vul.id, vul.strategy.vul_name)
    cache.delete(cache_key)
    #delete if exists more than one   departured use redis lock
    #IastVulnerabilityModel.objects.filter(
    #    strategy=vul_strategy.id,
    #    uri=method_pool.uri,
    #    http_method=method_pool.http_method,
    #    agent__in=project_agents,
    #    pk__lt=vul.id,
    #).delete()
