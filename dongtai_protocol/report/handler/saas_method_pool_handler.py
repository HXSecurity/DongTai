#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/5 下午12:36
# software: PyCharm
# project: lingzhi-webapi
import json
import logging
import random
import time
import uuid
from hashlib import sha256,sha1

import requests
from django.db import transaction

from dongtai_common.models.agent_method_pool import MethodPool
from dongtai_common.models.replay_method_pool import IastAgentMethodPoolReplay
from dongtai_common.models.replay_queue import IastReplayQueue
from dongtai_common.utils import const
from dongtai_common.models.res_header import (
    ProjectSaasMethodPoolHeader,
    HeaderType,
)
from dongtai_engine.tasks import search_vul_from_method_pool, search_vul_from_replay_method_pool
from dongtai_conf import settings
from dongtai_protocol import utils
from dongtai_protocol.report.handler.report_handler_interface import IReportHandler
from dongtai_protocol.report.report_handler_factory import ReportHandler
import gzip
import base64
from typing import Tuple
from django.core.cache import cache
logger = logging.getLogger('dongtai.openapi')


@ReportHandler.register(const.REPORT_VULN_SAAS_POOL)
class SaasMethodPoolHandler(IReportHandler):
    def __init__(self):
        super(SaasMethodPoolHandler, self).__init__()
        self.async_send = settings.config.getboolean('task', 'async_send', fallback=False)
        self.async_send_delay = settings.config.getint('task', 'async_send_delay', fallback=2)
        self.retryable = settings.config.getboolean('task', 'retryable', fallback=False)

        if self.async_send and (ReportHandler.log_service_disabled or ReportHandler.log_service is None):
            logger.error('log service disabled or failed to connect, disable async send method pool')
            self.async_send = False
        else:
            self.log_service = ReportHandler.log_service

    @staticmethod
    def parse_headers(headers_raw):
        headers = dict()
        header_raw = base64.b64decode(headers_raw).decode('utf-8').split('\n')
        item_length = len(header_raw)
        for index in range(item_length):
            _header_list = header_raw[index].split(':')
            _header_name = _header_list[0]
            headers[_header_name] = ':'.join(_header_list[1:])
        return headers

    def parse(self):
        self.version = self.report.get('version', 'v1')
        self.http_uri = self.detail.get('uri')
        self.http_url = self.detail.get('url')
        self.http_query_string = self.detail.get('queryString')
        self.http_req_data = self.detail.get('reqBody')
        self.http_req_header = self.detail.get('reqHeader')
        self.http_method = self.detail.get('method')
        self.http_scheme = self.detail.get('scheme')
        self.http_secure = self.detail.get('secure')
        self.http_protocol = self.detail.get('protocol')
        self.http_replay = self.detail.get('replayRequest')
        self.http_res_header = self.detail.get('resHeader')
        self.http_res_body = self.detail.get('resBody')
        self.context_path = self.detail.get('contextPath')
        self.client_ip = self.detail.get('clientIp')
        self.method_pool = self.report.get('detail', {}).get('pool', None)
        if self.method_pool:
            self.method_pool = sorted(self.method_pool,
                                      key=lambda e: e.__getitem__('invokeId'),
                                      reverse=True)
        logger.info(
            f"start record method_pool : {self.agent_id} {self.http_uri} {self.http_method}"
        )

    def save(self):
        """
        如果agent存在，保存数据
        :return:
        """
        headers = SaasMethodPoolHandler.parse_headers(self.http_req_header)
        save_project_header(headers.keys(), self.agent_id)
        add_new_api_route(self.agent_id, self.http_uri, self.http_method)
        if self.http_replay:
            # 保存数据至重放请求池
            replay_id = headers.get('dongtai-replay-id')
            replay_type = headers.get('dongtai-replay-type')
            relation_id = headers.get('dongtai-relation-id')
            timestamp = int(time.time())

            # fixme 直接查询replay_id是否存在，如果存在，直接覆盖
            query_set = IastAgentMethodPoolReplay.objects.values("id").filter(
                replay_id=replay_id)
            if query_set.exists():
                # 更新
                replay_model = query_set.first()
                replay_model.update(
                    url=self.http_url,
                    uri=self.http_uri,
                    req_header=self.http_req_header,
                    req_params=self.http_query_string,
                    req_data=self.http_req_data,
                    res_header=self.http_res_header,
                    res_body=decode_content(
                        get_res_body(self.http_res_body, self.version),
                        get_content_encoding(self.http_res_header),
                        self.version),
                    context_path=self.context_path,
                    method_pool=json.dumps(self.method_pool),
                    clent_ip=self.client_ip,
                    update_time=timestamp)
                method_pool_id = replay_model['id']
            else:
                # 新增
                replay_model = IastAgentMethodPoolReplay.objects.create(
                    agent=self.agent,
                    url=self.http_url,
                    uri=self.http_uri,
                    http_method=self.http_method,
                    http_scheme=self.http_scheme,
                    http_protocol=self.http_protocol,
                    req_header=self.http_req_header,
                    req_params=self.http_query_string,
                    req_data=self.http_req_data,
                    res_header=self.http_res_header,
                    res_body=decode_content(
                        get_res_body(self.http_res_body, self.version),
                        get_content_encoding(self.http_res_header),
                        self.version),
                    context_path=self.context_path,
                    method_pool=json.dumps(self.method_pool),
                    clent_ip=self.client_ip,
                    replay_id=replay_id,
                    replay_type=replay_type,
                    relation_id=relation_id,
                    create_time=timestamp,
                    update_time=timestamp)
                method_pool_id = replay_model.id
            IastReplayQueue.objects.filter(id=replay_id).update(
                state=const.SOLVED)
            if method_pool_id:
                logger.info(f"send replay method pool {self.agent_id} {self.http_uri} {method_pool_id} to celery ")
                self.send_to_engine(method_pool_id=method_pool_id,
                                    model='replay')
        else:
            pool_sign = uuid.uuid4().hex
            if self.async_send:
                try:
                    method_pool = self.to_json(pool_sign)
                    ok = self.log_service.send(method_pool)
                    if ok:
                        self.send_to_engine(method_pool_sign=pool_sign)
                except Exception as e:
                    logger.error(e, exc_info=True)
            else:
                current_version_agents = self.get_project_agents(self.agent)
                with transaction.atomic():
                    try:
                        update_record, method_pool = self.save_method_call(
                            pool_sign, current_version_agents)
                    except Exception as e:
                        logger.info(
                            f"record method failed : {self.agent_id} {self.http_uri} {self.http_method}"
                        )
                        logger.error(e, exc_info=True)
                try:
                    logger.info(f"send normal method pool {self.agent_id} {self.http_uri} {pool_sign} to celery ")
                    self.send_to_engine(method_pool_sign=pool_sign,
                                        update_record=update_record)
                except Exception as e:
                    logger.error(e, exc_info=True)

    def to_json(self, pool_sign: str):
        timestamp = int(time.time())
        pool = {
            'agent_id': self.agent_id,
            'url': self.http_url,
            'uri': self.http_uri,
            'http_method': self.http_method,
            'http_scheme': self.http_scheme,
            'http_protocol': self.http_protocol,
            'req_header': self.http_req_header,
            'req_params': self.http_query_string,
            'req_data': self.http_req_data,
            'req_header_for_search': utils.build_request_header(req_method=self.http_method,
                                                                raw_req_header=self.http_req_header,
                                                                uri=self.http_uri,
                                                                query_params=self.http_query_string,
                                                                http_protocol=self.http_protocol),
            'res_header': utils.base64_decode(self.http_res_header),
            'res_body': decode_content(get_res_body(self.http_res_body, self.version),
                                       get_content_encoding(self.http_res_header), self.version),
            'context_path': self.context_path,
            'method_pool': json.dumps(self.method_pool),
            'pool_sign': pool_sign,
            'clent_ip': self.client_ip,
            'create_time': timestamp,
            'update_time': timestamp,
            'uri_sha1': self.sha1(self.http_uri),
        }
        return json.dumps(pool)

    def save_method_call(self, pool_sign: str,
                         current_version_agents) -> Tuple[bool, MethodPool]:
        """
        保存方法池数据
        :param pool_sign:
        :param current_version_agents:
        :return:
        """
        # todo need to del
        # pool_sign = random.sample('zyxwvutsrqmlkjihgfedcba',5)
        method_pool = MethodPool.objects.filter(
            pool_sign=pool_sign, agent__in=current_version_agents).first()
        update_record = True
        if method_pool:
            method_pool.update_time = int(time.time())
            method_pool.method_pool = json.dumps(self.method_pool)
            method_pool.uri = self.http_uri
            method_pool.url = self.http_url
            method_pool.http_method = self.http_method
            method_pool.req_header = self.http_req_header
            method_pool.req_params = self.http_query_string
            method_pool.req_data = self.http_req_data
            method_pool.req_header_fs = utils.build_request_header(
                req_method=self.http_method,
                raw_req_header=self.http_req_header,
                uri=self.http_uri,
                query_params=self.http_query_string,
                http_protocol=self.http_protocol)
            method_pool.res_header = utils.base64_decode(self.http_res_header)
            method_pool.res_body = decode_content(
                get_res_body(self.http_res_body, self.version),
                get_content_encoding(self.http_res_header), self.version)
            method_pool.uri_sha1 = self.sha1(self.http_uri)
            method_pool.save(update_fields=[
                'update_time',
                'method_pool',
                'uri',
                'url',
                'http_method',
                'req_header',
                'req_params',
                'req_data',
                'req_header_fs',
                'res_header',
                'res_body',
                'uri_sha1',
            ])
        else:
            # 获取agent
            update_record = False
            timestamp = int(time.time())
            method_pool = MethodPool.objects.create(
                agent=self.agent,
                url=self.http_url,
                uri=self.http_uri,
                http_method=self.http_method,
                http_scheme=self.http_scheme,
                http_protocol=self.http_protocol,
                req_header=self.http_req_header,
                req_params=self.http_query_string,
                req_data=self.http_req_data,
                req_header_fs=utils.build_request_header(
                    req_method=self.http_method,
                    raw_req_header=self.http_req_header,
                    uri=self.http_uri,
                    query_params=self.http_query_string,
                    http_protocol=self.http_protocol),
                res_header=utils.base64_decode(self.http_res_header),
                res_body = decode_content(
                get_res_body(self.http_res_body, self.version),
                get_content_encoding(self.http_res_header),self.version),
                context_path=self.context_path,
                method_pool=json.dumps(self.method_pool),
                pool_sign=pool_sign,
                clent_ip=self.client_ip,
                create_time=timestamp,
                update_time=timestamp,
                uri_sha1=self.sha1(self.http_uri),
            )
        return update_record, method_pool

    def send_to_engine(self, method_pool_id="", method_pool_sign="", update_record=False, model=None):
        try:
            if model is None:
                logger.info(
                    f'[+] send method_pool [{method_pool_sign}] to engine for {"update" if update_record else "new record"}')
                delay = 0
                if self.async_send:
                    delay = self.async_send_delay
                kwargs = {
                    'method_pool_sign': method_pool_sign,
                    'agent_id': self.agent_id,
                    'retryable': self.retryable,
                }
                res = search_vul_from_method_pool.apply_async(kwargs=kwargs, countdown=delay)
                logger.info(
                        f'[+] send method_pool [{method_pool_sign}] to engine for task search_vul_from_method_pool id: {res.task_id}')
                res = search_sink_from_method_pool.apply_async(kwargs=kwargs, countdown=delay)
                logger.info(
                        f'[+] send method_pool [{method_pool_sign}] to engine for task search_sink_from_strategy id: {res.task_id}')
            else:
                logger.info(
                    f'[+] send method_pool [{method_pool_id}] to engine for {model if model else ""}'
                )
                res = search_vul_from_replay_method_pool.delay(method_pool_id)
                logger.info(
                    f'[+] send method_pool [{method_pool_id}] to engine for task search_vul_from_replay_method_pool id: {res.task_id}'
                )
                #requests.get(url=settings.REPLAY_ENGINE_URL.format(id=method_pool_id))
        except Exception as e:
            logger.error(f'[-] Failure: send method_pool [{method_pool_id}{method_pool_sign}], Error: {e}')

    def calc_hash(self):
        sign_raw = '-'.join(
            filter(lambda x: x, [
                getattr(self, i, '')
                for i in ('http_uri', 'http_method', 'http_req_header',
                          'http_req_params', 'http_req_data')
            ]))
        for method in self.method_pool:
            sign_raw += f"{method.get('className')}.{method.get('methodName')}()->"
        sign_sha256 = self.sha256(sign_raw)
        return sign_sha256

    @staticmethod
    def sha1(raw):
        h = sha1()
        h.update(raw.encode('utf-8'))
        return h.hexdigest()

    @staticmethod
    def sha256(raw):
        h = sha256()
        h.update(raw.encode('utf-8'))
        return h.hexdigest()


from dongtai_common.models.api_route import (IastApiRoute, IastApiMethod,
                                             FromWhereChoices)
from django.db.utils import IntegrityError


def save_project_header(keys: list, agent_id: int):
    uuid_key = uuid.uuid4().hex
    keys = list(
        filter(
            lambda key: uuid_key == cache.get_or_set(
                f'project_header-{agent_id}-{key}', uuid_key, 60 * 5), keys))
    objs = [
        ProjectSaasMethodPoolHeader(key=key,
                                    agent_id=agent_id,
                                    header_type=HeaderType.REQUEST)
        for key in keys
    ]
    if not keys:
        return
    ProjectSaasMethodPoolHeader.objects.bulk_create(objs,
                                                    ignore_conflicts=True)


def add_new_api_route(agent_id, path, method):
    logger.info(f"{agent_id}, {path}, {method}")
    uuid_key = uuid.uuid4().hex
    is_api_cached = uuid_key != cache.get_or_set(
        f'api_route-{agent_id}-{path}-{method}', uuid_key, 60 * 5)
    if is_api_cached:
        logger.info(
            f"found cache api_route-{agent_id}-{path}-{method} ,skip its insert"
        )
        return
    try:
        api_method, is_create = IastApiMethod.objects.get_or_create(
            method=method.upper())
        api_route, is_create = IastApiRoute.objects.get_or_create(
            from_where=FromWhereChoices.FROM_METHOD_POOL,
            method_id=api_method.id,
            path=path,
            agent_id=agent_id)

    except IntegrityError as e:
        logger.error(e)

def decode_content(body, content_encoding, version):
    if version == 'v1':
        return body
    if content_encoding == 'gzip':
        try:
            return gzip.decompress(body).decode('utf-8')
        except:
            logger.error('not gzip type but using gzip as content_encoding')
    # TODO not content_encoding
    if content_encoding:
        logger.info('not found content_encoding :{}'.format(content_encoding))
    try:
        return body.decode('utf-8')
    except:
        logger.info('decode_content, {}'.format(body))
        logger.info('utf-8 decode failed, use raw ')
        return body.decode('raw_unicode_escape')


def get_content_encoding(b64_res_headers):
    res_headers = utils.base64_decode(b64_res_headers)
    for header in res_headers.split('\n'):
        try:
            k, v = [i.strip().lower() for i in header.split(':')]
            if k == "content-encoding":
                if 'gzip' in v:
                    return 'gzip'
                break
        except:
            pass
    return ''


def get_res_body(res_body, version):
    if version == 'v1':
        return res_body  #bytes
    elif version == 'v2':
        return base64.b64decode(res_body)  #bytes
    logger.info('no match version now version: {}'.format(version))
    return res_body
