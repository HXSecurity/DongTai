#!/usr/bin/env python
import logging
from collections import defaultdict
from functools import reduce

from django.core.cache import cache
from django.db.models import Q
from django.forms.models import model_to_dict
from django.utils.translation import gettext_lazy as _

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.agent import IastAgent
from dongtai_web.serializers.agent import AgentSerializer
from dongtai_web.utils import (
    extend_schema_with_envcheck,
    get_model_field,
    get_response_serializer,
)

logger = logging.getLogger("dongtai-webapi")

_ResponseSerializer = get_response_serializer(
    data_serializer=AgentSerializer(many=True),
)


class AgentList(UserEndPoint):
    name = "api-v1-agents"
    description = _("Agent list")
    SERVER_MAP = {}

    def get_running_status(self, obj):
        mapping = defaultdict(str)
        mapping.update({1: _("Online"), 0: _("Offline")})
        return mapping[obj.online]

    def get_server(self, obj):
        def get_server_addr():
            if obj.server_id not in self.SERVER_MAP:
                if obj.server.ip and obj.server.port and obj.server.port != 0:
                    self.SERVER_MAP[obj.server_id] = f"{obj.server.ip}:{obj.server.port}"
                else:
                    return _("No flow is detected by the probe")
            return self.SERVER_MAP[obj.server_id]

        if obj.server_id:
            return get_server_addr()
        return _("No flow is detected by the probe")

    def make_key(self, request):
        self.cache_key = f"{request.user.id}_total_agent_id"
        self.cache_key_max_id = f"{request.user.id}_max_agent_id"

    def get_query_cache(self):
        total = cache.get(self.cache_key)
        max_id = cache.get(self.cache_key_max_id)
        return total, max_id

    def set_query_cache(self, q):
        total = IastAgent.objects.filter(q).count()
        if total > 0:
            max_id = IastAgent.objects.filter(q).values_list("id", flat=True).order_by("-id")[0]
        else:
            max_id = 0
        cache.set(self.cache_key, total, 60 * 60)
        cache.set(self.cache_key_max_id, max_id, 60 * 60)
        return total, max_id

    def parse_args(self, request):
        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("pageSize", 20))
        page_size = page_size if page_size < 50 else 50
        return page, page_size, request.user

    @extend_schema_with_envcheck(
        [
            {
                "name": "page",
                "type": int,
                "default": 1,
                "required": False,
            },
            {
                "name": "pageSize",
                "type": int,
                "default": 1,
                "required": False,
            },
            {
                "name": "state",
                "type": int,
                "default": 1,
                "required": False,
            },
            {
                "name": "token",
                "type": str,
                "required": False,
            },
            {
                "name": "project_name",
                "type": str,
                "required": False,
            },
        ],
        tags=[_("Agent")],
        summary=_("Agent List"),
        description=_("Get a list containing Agent information according to conditions."),
        response_schema=_ResponseSerializer,
    )
    def get(self, request):
        try:
            page = int(request.query_params.get("page", 1))
            page_size = int(request.query_params.get("pageSize", 20))
            running_state = request.query_params.get("state", None)
            if running_state is not None:
                running_state = int(running_state)
            project_id = request.query_params.get("project_id", None)
            if project_id:
                project_id = int(project_id)

            fields = get_model_field(
                IastAgent,
                include=["token", "project_name"],
            )
            searchfields = dict(filter(lambda k: k[0] in fields, request.query_params.items()))
            searchfields_ = {k: v for k, v in searchfields.items() if k in fields}
            q = reduce(
                lambda x, y: x | y,
                (
                    Q(**x)
                    for x in ({"__".join([kv_pair[0], "icontains"]): kv_pair[1]} for kv_pair in searchfields_.items())
                ),
                Q(),
            )
            if running_state is not None:
                q = q & Q(online=running_state)
            if request.user.is_superuser == 1:
                pass
            elif request.user.is_superuser == 2:
                q = q & Q(user__in=self.get_auth_users(request.user))
            else:
                q = q & Q(user_id=request.user.id)
            if project_id:
                q = q & Q(bind_project_id=project_id)

            self.make_key(request)
            if page == 1:
                total, max_id = self.set_query_cache(q)
            else:
                total, max_id = self.get_query_cache()
                if not total or not max_id:
                    total, max_id = self.set_query_cache(q)

            if page > 1:
                before_id = page * page_size
                q = q & Q(id__gt=before_id)
            baseQuery = IastAgent.objects.filter(q)
            cur_data = (
                baseQuery.filter(id__lte=max_id)
                .values_list("id", flat=True)
                .order_by("-id")[(page - 1) * page_size : page * page_size]
            )
            cur_ids = list(cur_data)

            queryset = (
                IastAgent.objects.filter(id__in=cur_ids)
                .order_by("-id")
                .select_related("server", "user")
                .prefetch_related("heartbeats")
            )
            end = []
            for item in queryset:
                one = model_to_dict(item)  # type: ignore
                server_data = model_to_dict(item.server)
                one["cluster_name"] = server_data.get("cluster_name", "")
                one["cluster_version"] = server_data.get("cluster_version", "")
                one["owner"] = item.user.username
                one["server"] = self.get_server(item)
                if not one.get("alias", ""):
                    one["alias"] = one["token"]
                all = item.heartbeats.all()
                if all:
                    one["report_queue"] = all[0].report_queue
                    one["method_queue"] = all[0].method_queue
                    one["replay_queue"] = all[0].replay_queue
                    one["system_load"] = all[0].cpu
                    one["flow"] = all[0].req_count
                    one["latest_time"] = all[0].dt
                else:
                    one["report_queue"] = 0
                    one["method_queue"] = 0
                    one["replay_queue"] = 0
                    one["system_load"] = _("Load data is not uploaded")
                    one["flow"] = 0
                del one["online"]
                one["running_status"] = self.get_running_status(item)
                end.append(one)

            # if not request.user.is_talent_admin():
            page_info = {"alltotal": total, "num_pages": page, "page_size": page_size}
            return R.success(msg="success", data=end, page=page_info)
        except ValueError as e:
            logger.error(e, exc_info=True)
            return R.failure(msg=_("Incorrect format parameter, please check again"))
        except Exception as e:
            logger.error(e, exc_info=True)
            return R.failure(msg=_("Program error"))


def removestartup(dic):
    del dic["startup_time"]
    return dic
