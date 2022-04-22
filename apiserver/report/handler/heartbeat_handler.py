#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/10/23 11:56
# software: PyCharm
# project: webapi
import logging
import time

from dongtai.models.agent import IastAgent
from dongtai.models.heartbeat import IastHeartbeat
from dongtai.models.replay_queue import IastReplayQueue
from dongtai.models.vulnerablity import IastVulnerabilityModel
from dongtai.utils import const
from django.utils.translation import gettext_lazy as _
from dongtai.models.server import IastServer
from apiserver.report.handler.report_handler_interface import IReportHandler
from apiserver.report.report_handler_factory import ReportHandler
from django.db.models import (QuerySet, Q, F)

logger = logging.getLogger('dongtai.openapi')


@ReportHandler.register(const.REPORT_HEART_BEAT)
class HeartBeatHandler(IReportHandler):
    def __init__(self):
        super().__init__()
        self.req_count = None
        self.cpu = None
        self.memory = None
        self.network = None
        self.report_queue = None
        self.method_queue = None
        self.replay_queue = None
        self.return_queue = None


    def parse(self):
        self.cpu = self.detail.get('cpu')
        self.memory = self.detail.get('memory')
        self.req_count = self.detail.get('reqCount')
        self.report_queue = self.detail.get('reportQueue', 0)
        self.method_queue = self.detail.get('methodQueue', 0)
        self.replay_queue = self.detail.get('replayQueue', 0)
        self.return_queue = self.detail.get('returnQueue', None)

    def has_permission(self):
        self.agent = IastAgent.objects.filter(id=self.agent_id, user=self.user_id).first()
        return self.agent

    def has_permission(self):
        self.agent = IastAgent.objects.filter(id=self.agent_id, user=self.user_id).first()
        return self.agent

    def save_heartbeat(self):
        # update agent state
        self.agent.is_running = 1
        self.agent.online = 1
        self.agent.save(update_fields=['is_running', 'online'])
        queryset = IastHeartbeat.objects.filter(agent=self.agent)
        heartbeat = queryset.order_by('-id').first()
        if heartbeat:
            queryset.exclude(pk=heartbeat.id).delete()
            heartbeat.dt = int(time.time())
            if self.return_queue == 1:
                heartbeat.req_count = self.req_count
                heartbeat.report_queue = self.report_queue
                heartbeat.method_queue = self.method_queue
                heartbeat.replay_queue = self.replay_queue
                heartbeat.save(update_fields=[
                    'req_count', 'dt', 'report_queue', 'method_queue', 'replay_queue'
                ])
            elif self.return_queue == 0:
                heartbeat.memory = self.memory
                heartbeat.cpu = self.cpu
                heartbeat.save(update_fields=[
                    'memory','cpu', 'dt'
                ])
            else:
                heartbeat.memory = self.memory
                heartbeat.cpu = self.cpu
                heartbeat.req_count = self.req_count
                heartbeat.report_queue = self.report_queue
                heartbeat.method_queue = self.method_queue
                heartbeat.replay_queue = self.replay_queue
                heartbeat.save(update_fields=[
                    'memory', 'cpu', 'req_count', 'dt', 'report_queue', 'method_queue', 'replay_queue'
                ])
        else:
            IastHeartbeat.objects.create(memory=self.memory,
                                         cpu=self.cpu,
                                         req_count=self.req_count,
                                         report_queue=self.replay_queue,
                                         method_queue=self.method_queue,
                                         replay_queue=self.replay_queue,
                                         dt=int(time.time()),
                                         agent=self.agent)

    def get_result(self, msg=None):
        logger.info('return_queue: {}'.format(self.return_queue))
        print('return_queue: {}'.format(self.return_queue))
        print("="*20)
        if self.return_queue is None or self.return_queue == 1:
            try:
                project_agents = IastAgent.objects.values('id').filter(
                    bind_project_id=self.agent.bind_project_id)
                #project_agents = project_agents.union(*[
                #    addtional_agenti_ids_query_filepath_simhash(
                #        self.agent.filepathsimhash),
                #], all=True)
                project_agents = list(
                    set(
                        IastAgent.objects.values_list('id', flat=True).filter(
                            bind_project_id=self.agent.bind_project_id)
                        | addtional_agenti_ids_query_filepath_simhash(
                            self.agent.filepathsimhash)
                        | addtional_agent_ids_query_deployway_and_path(
                            self.agent.servicetype, self.agent.server.path,
                            self.agent.server.hostname)))
                if project_agents is None:
                    logger.info(_('There is no probe under the project'))
                replay_queryset = IastReplayQueue.objects.values(
                    'id', 'relation_id', 'uri', 'method', 'scheme', 'header',
                    'params', 'body', 'replay_type').filter(
                        agent_id__in=project_agents,
                        state__in=[const.WAITING, const.SOLVING])[:200]
                if len(replay_queryset) == 0:
                    logger.info(_('Replay request does not exist'))

                (success_ids, success_vul_ids, failure_ids, failure_vul_ids,
                 replay_requests) = ([], [], [], [], [])
                for replay_request in replay_queryset:
                    if replay_request['uri']:
                        replay_requests.append(replay_request)
                        success_ids.append(replay_request['id'])
                        if replay_request['replay_type'] == const.VUL_REPLAY:
                            success_vul_ids.append(replay_request['relation_id'])
                    else:
                        failure_ids.append(replay_request['id'])
                        if replay_request['replay_type'] == const.VUL_REPLAY:
                            failure_vul_ids.append(replay_request['relation_id'])

                timestamp = int(time.time())
                IastReplayQueue.objects.filter(id__in=success_ids).update(update_time=timestamp, state=const.SOLVING)
                IastReplayQueue.objects.filter(id__in=failure_ids).update(update_time=timestamp, state=const.SOLVED)

                IastVulnerabilityModel.objects.filter(id__in=success_vul_ids).update(latest_time=timestamp, status_id=2)
                IastVulnerabilityModel.objects.filter(id__in=failure_vul_ids).update(latest_time=timestamp, status_id=1)
                logger.info(_('Reproduction request issued successfully'))

                return replay_requests
            except Exception as e:
                print(e)
                logger.info(
                    _('Replay request query failed, reason: {}').format(e),
                    exc_info=True)

        return list()

    def save(self):
        self.save_heartbeat()


def get_k8s_deployment_id(hostname: str) -> str:
    return hostname[hostname.rindex('-')]


def addtional_agent_ids_query_deployway_and_path(deployway: str, path: str,
                                                 hostname: str) -> QuerySet:
    if deployway == 'k8s':
        deployment_id = get_k8s_deployment_id(hostname)
        print(deployment_id)
        server_q = Q(server__hostname__startswith=deployment_id) & Q(server__path=path) & Q(
            server__path='') & ~Q(server__hostname='')
    elif deployway == 'docker':
        server_q = Q(server__path=path) & ~Q(server__path='')
    else:
        server_q = Q(server__path=str(path)) & Q(server__hostname=str(
            hostname)) & ~Q(server__path='') & ~Q(server__hostname='')
    final_q = server_q
    return IastAgent.objects.filter(final_q).values_list('id',flat=True)


def addtional_agenti_ids_query_filepath_simhash(
        filepathsimhash: str) -> QuerySet:
    return IastAgent.objects.filter(filepathsimhash=filepathsimhash).values_list(
        'id', flat=True)
