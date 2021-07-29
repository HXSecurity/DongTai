import json
import logging

from dongtai.endpoint import R, AnonymousAndUserEndPoint
from dongtai.engine.vul_engine import VulEngine
from dongtai.models.agent_method_pool import MethodPool
from dongtai.models.agent import IastAgent
from dongtai.models.project import IastProject
from dongtai.models.user import User
from dongtai.models.vulnerablity import IastVulnerabilityModel
from iast.serializers.method_pool import MethodPoolListSerialize
from django.db.models import Q
from django.forms.models import model_to_dict
from iast.utils import get_model_field
from functools import reduce
from dongtai.models.agent import IastAgent
from dongtai.models.heartbeat import IastHeartbeat
from dongtai.models.server import IastServer
from django.core.paginator import Paginator
from iast.serializers.agent import AgentSerializer

class AgentSearch(AnonymousAndUserEndPoint):
    def get(self, request):
        page_size = int(request.query_params.get('page_size', 10))
        page = int(request.query_params.get('page', 1))
        fields = get_model_field(
            IastAgent,
            include=['token', 'project_name'],
        )
        searchfields = dict(
            filter(lambda k: k[0] in fields, request.query_params.items()))
        searchfields_ = {k: v for k, v in searchfields.items() if k in fields}
        q = reduce(
            lambda x, y: x | y,
            map(
                lambda x: Q(**x),
                map(
                    lambda kv_pair:
                    {'__'.join([kv_pair[0], 'contains']): kv_pair[1]},
                    searchfields_.items())), Q())
        queryset = IastAgent.objects.filter(q).order_by('-latest_time').all()
        summary, agents = self.get_paginator(queryset, page, page_size)
        paginator = Paginator(queryset, page_size)
        summary = {"alltotal": paginator.count, "num_pages": paginator.num_pages, "page_size": page_size}
        agents = paginator.page(page).object_list
        agents = list(agents.values())
        servers = IastServer.objects.filter(pk__in=[_['server_id']for _ in agents]).all().values()
        heartbeats = IastHeartbeat.objects.filter(agent_id__in=[_['id'] for _ in agents]).all().values()
        servers = {_['id']: _ for _ in servers}
        heartbeats = {_['agent_id']: _ for _ in heartbeats}
        relations = []
        for agent in agents:
            item = {}
            item['agent_id'] = agent['id']
            server = servers.get(agent['server_id'], None)
            if server:
                for k, v in server.items():
                    item['_'.join(['server', k])] = v
            heartbeat = heartbeats.get(agent['id'], None)
            if heartbeat:
                for k, v in heartbeat.items():
                    item['_'.join(['heartbeat', k])] = v
            relations.append(item)
        return R.success(
            data={
                'agents': agents,
                'summary': summary,
                'relations': relations,
            })
