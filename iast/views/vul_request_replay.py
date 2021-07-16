#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/23 下午2:16
# software: PyCharm
# project: lingzhi-webapi
import logging
from http.server import BaseHTTPRequestHandler
from io import BytesIO
import base64
import time
from dongtai.models.agent_method_pool import MethodPool
from dongtai.models.replay_method_pool import IastAgentMethodPoolReplay
from dongtai.models.replay_queue import IastReplayQueue
from dongtai.utils import const

from base import R
from iast.base.user import UserEndPoint

logger = logging.getLogger('dongtai-webapi')


class HttpRequest(BaseHTTPRequestHandler):
    def __init__(self, raw_request):
        self.body = None
        self.uri = None
        self.params = None
        self.rfile = BytesIO(raw_request.encode())
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.parse_request()
        self.parse_path()
        self.parse_body()

    def parse_body(self):
        if self.body is None:
            self.body = self.rfile.read().decode('utf-8')
        return self.body

    def parse_path(self):
        items = self.path.split('?')
        self.uri = items[0]
        self.params = '?'.join(items[1:])


class RequestReplayEndPoint(UserEndPoint):

    @staticmethod
    def check_replay_request(raw_request):
        """
        检查重放请求是否符合要求：不存在恶意攻击数据
        :param replay_request:
        :return:
        """
        try:
            replay_request = HttpRequest(raw_request=raw_request)
            requests = {
                'method': replay_request.command,
                'uri': replay_request.uri,
                'params': replay_request.params,
                'scheme': replay_request.request_version,
                'header': base64.b64encode(replay_request.headers.as_string().strip().encode()).decode(),
                'body': replay_request.body,
            }

            return False, requests
        except Exception as e:
            logger.error(f'HTTP请求解析出错，原因：{e}')
            return True, None

    @staticmethod
    def check_method_pool(method_pool_id, user):
        """
        检查方法池数据是否符合重放要求：方法池存在及用户有操作权限
        :param method_pool_id: 方法池ID
        :param user: 用户对象
        :return:
            status: True - 方法池存在且用户可操作；False - 方法池不存在或用户无权限操作
            model: 方法池对象；None
        """
        if method_pool_id is None or method_pool_id == '':
            return True, None

        auth_agents = RequestReplayEndPoint.get_auth_agents_with_user(user)
        method_pool_model = MethodPool.objects.filter(id=method_pool_id, agent__in=auth_agents).first()
        if method_pool_model:
            return False, method_pool_model
        else:
            return True, None

    @staticmethod
    def check_agent_active(agent):
        """
        检查agent是否为存活状态：agent及检测引擎均在运行中
        :param agent: agent对象
        :return: True - 未存活；False - 存活
        """
        return agent.is_running == 0 or agent.is_core_running == 0

    @staticmethod
    def send_request_to_replay_queue(relation_id, agent_id, replay_request):
        """
        发送重放请求到重放队列
        :param replay_request: 重放请求数据
        :param method_pool_model: 重放的方法池
        :return: 0-成功、1-正在重放中
        """
        timestamp = int(time.time())
        replay_queue = IastReplayQueue.objects.filter(
            replay_type=const.REQUEST_REPLAY,
            relation_id=relation_id
        ).first()
        if replay_queue:
            if replay_queue.state not in [const.WAITING, const.SOLVING]:
                replay_queue.state = const.WAITING
                replay_queue.uri = replay_request['uri']
                replay_queue.method = replay_request['method']
                replay_queue.scheme = replay_request['scheme']
                replay_queue.header = replay_request['header']
                replay_queue.params = replay_request['params']
                replay_queue.body = replay_request['body']
                replay_queue.update_time = timestamp
                replay_queue.agent_id = agent_id
                replay_queue.save(
                    update_fields=['uri', 'method', 'scheme', 'header', 'params', 'body', 'update_time', 'agent_id',
                                   'state', 'agent_id'])
        else:
            replay_queue = IastReplayQueue.objects.create(
                relation_id=relation_id,
                replay_type=const.REQUEST_REPLAY,
                state=const.WAITING,
                uri=replay_request['uri'],
                method=replay_request['method'],
                scheme=replay_request['scheme'],
                header=replay_request['header'],
                params=replay_request['params'],
                body=replay_request['body'],
                create_time=timestamp,
                count=0,
                update_time=timestamp,
                agent_id=agent_id,
            )
        return replay_queue.id

    def post(self, request):
        """
        查找项目中存在活跃探针的数量
        :param request:{
            'id':vul_id,
            'request': 'header'
        }
        :return:
        """
        try:
            method_pool_id = request.data.get('methodPoolId')
            replay_request = request.data.get('replayRequest')

            check_failure, method_pool_model = self.check_method_pool(method_pool_id, request.user)
            if check_failure:
                return R.failure(msg='污点池数据不存在或无权操作')

            check_failure = self.check_agent_active(method_pool_model.agent)
            if check_failure:
                return R.failure(msg='探针已销毁或暂停运行，请选检查探针状态')

            check_failure, checked_request = self.check_replay_request(raw_request=replay_request)
            if check_failure:
                return R.failure(msg='重放请求不合法')

            replay_id = self.send_request_to_replay_queue(
                relation_id=method_pool_model.id,
                agent_id=method_pool_model.agent.id,
                replay_request=checked_request
            )
            return R.success(msg='请求重返成功', data={'replayId': replay_id})

        except Exception as e:
            return R.failure(msg=f'漏洞重放出错，错误原因：{e}')

    @staticmethod
    def check_replay_data_permission(replay_id, auth_agents):
        return IastReplayQueue.objects.values('id').filter(id=replay_id, agent__in=auth_agents).exists()

    @staticmethod
    def parse_response(header, body):
        try:
            _data = base64.b64decode(header.encode("utf-8")).decode("utf-8")
        except Exception as e:
            _data = ''
            logger.error(f'Response Header解析出错，错误原因：{e}')
        return '{header}\n\n{body}'.format(header=_data, body=body)

    def get(self, request):
        replay_id = request.query_params.get('replayId')
        auth_agents = self.get_auth_agents_with_user(request.user)

        has_permission = self.check_replay_data_permission(replay_id=replay_id, auth_agents=auth_agents)
        if has_permission is False:
            return R.failure(msg='重放请求不存在或无操作权限')

        # 查询响应体
        replay_data = IastAgentMethodPoolReplay.objects.filter(replay_id=replay_id,
                                                               replay_type=const.REQUEST_REPLAY).values(
            'res_header', 'res_body', 'method_pool').first()
        # todo 调用污点链构造方法，构造污点链
        if replay_data:
            return R.success(data={
                'response': self.parse_response(replay_data['res_header'], replay_data['res_body']),
                'graph': ''
            })
        else:
            return R.failure(msg='重放请求处理中')
