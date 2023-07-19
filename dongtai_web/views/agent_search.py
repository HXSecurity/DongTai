from functools import reduce

from django.db.models import Q
from django.forms.models import model_to_dict
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from dongtai_common.endpoint import AnonymousAndUserEndPoint, R
from dongtai_common.models.agent import IastAgent
from dongtai_common.models.heartbeat import IastHeartbeat
from dongtai_common.models.server import IastServer
from dongtai_web.utils import extend_schema_with_envcheck, get_model_field, get_response_serializer


class _AgentSearchQuerysSerializer(serializers.Serializer):
    page_size = serializers.IntegerField(default=20, help_text=_("Number per page"))
    page = serializers.IntegerField(default=1, help_text=_("Page index"))
    token = serializers.CharField(help_text=_("The name of agent"))
    project_name = serializers.CharField(
        help_text=_(
            "Project name, used to start the agent first and then create the project"
        )
    )


_ResponseSerializer = get_response_serializer(
    status_msg_keypair=(((201, _("Suspending ...")), ""),)
)


class AgentSearch(AnonymousAndUserEndPoint):
    @extend_schema_with_envcheck(
        [_AgentSearchQuerysSerializer],
        tags=[_("Agent")],
        summary=_("Agent Search"),
        description=_(
            "Search for the agent corresponding to the user according to the following parameters"
        ),
        response_schema=_ResponseSerializer,
    )
    def get(self, request):
        page_size = int(request.query_params.get("page_size", 10))
        page = int(request.query_params.get("page", 1))
        fields = get_model_field(
            IastAgent,
            include=["token", "project_name"],
        )
        searchfields = dict(
            filter(lambda k: k[0] in fields, request.query_params.items())
        )
        searchfields_ = {k: v for k, v in searchfields.items() if k in fields}
        q = reduce(
            lambda x, y: x | y,
            (Q(**x) for x in ({"__".join([kv_pair[0], "icontains"]): kv_pair[1]} for kv_pair in searchfields_.items())),
            Q(),
        )
        agents = self.get_auth_and_anonymous_agents(request.user)
        q = q & Q(id__in=[_["id"] for _ in agents])
        queryset = IastAgent.objects.filter(q).order_by("-latest_time").all()
        summary, agents = self.get_paginator(queryset, page, page_size)
        servers = (
            IastServer.objects.filter(pk__in=[_["server_id"] for _ in agents])
            .all()
            .values()
        )
        heartbeats = (
            IastHeartbeat.objects.filter(agent_id__in=[_["id"] for _ in agents])
            .all()
            .values()
        )
        servers = {_["id"]: _ for _ in servers}
        heartbeats = {_["agent_id"]: _ for _ in heartbeats}
        relations = []
        for agent in agents:
            item = {}
            item["agent_id"] = agent["id"]
            server = servers.get(agent["server_id"], None)
            if server:
                for k, v in server.items():
                    item[f"server_{k}"] = v
            heartbeat = heartbeats.get(agent["id"], None)
            if heartbeat:
                for k, v in heartbeat.items():
                    item[f"heartbeat_{k}"] = v
            relations.append(item)
        return R.success(
            data={
                "agents": [model_to_dict(agent) for agent in agents],
                "summary": summary,
                "relations": relations,
            }
        )
