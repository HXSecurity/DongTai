#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi
import logging
from http.server import BaseHTTPRequestHandler
from io import BytesIO
import base64
import time
from dongtai_common.models.agent_method_pool import MethodPool
from dongtai_common.models.replay_method_pool import IastAgentMethodPoolReplay
from dongtai_common.models.replay_queue import IastReplayQueue
from dongtai_common.models.user import User
from dongtai_common.utils import const
from dongtai_common.models.agent import IastAgent
from dongtai_common.endpoint import R
from dongtai_common.endpoint import UserEndPoint
from django.utils.translation import gettext_lazy as _
from collections import namedtuple
from dongtai_web.utils import extend_schema_with_envcheck

logger = logging.getLogger("dongtai-webapi")


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
            self.body = self.rfile.read().decode("utf-8")
        return self.body

    def parse_path(self):
        items = self.path.split("?")
        self.uri = items[0]
        self.params = "?".join(items[1:])


class RequestReplayEndPoint(UserEndPoint):
    @staticmethod
    def check_replay_request(raw_request):
        """
        :param replay_request:
        :return:
        """
        try:
            replay_request = HttpRequest(raw_request=raw_request)
            requests = {
                "method": replay_request.command,
                "uri": replay_request.uri,
                "params": replay_request.params,
                "scheme": replay_request.request_version,
                "header": base64.b64encode(
                    replay_request.headers.as_string().strip().encode()
                ).decode(),
                "body": replay_request.body,
            }

            return False, requests
        except Exception as e:
            logger.error(_("HTTP request parsing error, error message: {}").format(e))
            return True, None

    @staticmethod
    def check_method_pool(method_pool_id, user):
        """
        :param method_pool_id:
        :param user:
        :return:
            status: True；False
            model: methodpool;None
        """
        if method_pool_id is None or method_pool_id == "":
            return True, None

        auth_agents = RequestReplayEndPoint.get_auth_agents_with_user(user)
        if method_pool_id == -1:
            method_pool_model = namedtuple("method_pool_model", ["id", "agent"])
            agent = namedtuple("agent", ["id", "is_running"])
            agent.id = 0
            agent.is_running = 0
            method_pool_model.agent = agent
            method_pool_model.id = -1
        else:
            method_pool_model = MethodPool.objects.filter(
                id=method_pool_id, agent__in=auth_agents
            ).first()
        if method_pool_model:
            return False, method_pool_model
        else:
            return True, None

    @staticmethod
    def check_agent_active(agent):
        """
        :param agent:
        :return: True  ；False
        """
        if not agent:
            return True
        return agent.online == 0

    @staticmethod
    def send_request_to_replay_queue(
        relation_id, agent_id, replay_request, replay_type
    ):
        """
        :param replay_request:
        :param method_pool_model:
        :return: 0、1
        """
        timestamp = int(time.time())
        replay_queue = IastReplayQueue.objects.filter(
            replay_type=replay_type, relation_id=relation_id, agent_id=agent_id
        ).first()
        if replay_queue:
            if replay_queue.state not in [
                const.WAITING,
            ]:
                replay_queue.state = const.WAITING
                replay_queue.uri = replay_request["uri"]
                replay_queue.method = replay_request["method"]
                replay_queue.scheme = replay_request["scheme"]
                replay_queue.header = replay_request["header"]
                replay_queue.params = replay_request["params"]
                replay_queue.body = replay_request["body"]
                replay_queue.update_time = timestamp
                replay_queue.agent_id = agent_id
                replay_queue.save(
                    update_fields=[
                        "uri",
                        "method",
                        "scheme",
                        "header",
                        "params",
                        "body",
                        "update_time",
                        "agent_id",
                        "state",
                        "agent_id",
                    ]
                )
                IastAgentMethodPoolReplay.objects.filter(
                    replay_id=replay_queue.id, replay_type=replay_type
                ).delete()
        else:
            replay_queue = IastReplayQueue.objects.create(
                relation_id=relation_id,
                replay_type=replay_type,
                state=const.WAITING,
                uri=replay_request["uri"],
                method=replay_request["method"],
                scheme=replay_request["scheme"],
                header=replay_request["header"],
                params=replay_request["params"],
                body=replay_request["body"],
                create_time=timestamp,
                count=0,
                update_time=timestamp,
                agent_id=agent_id,
            )
        return replay_queue.id

    @extend_schema_with_envcheck(
        [],
        {
            "methodPoolId": "int",
            "replayRequest": "str",
            "agent_id": "int",
            "replay_type": "int",
        },
        tags=["重放"],
        summary="请求包重放",
    )
    def post(self, request):
        """
        :param request:{
            'id':vul_id,
            'request': 'header'
        }
        :return:
        """
        try:
            method_pool_id = request.data.get("methodPoolId")
            replay_request = request.data.get("replayRequest")
            agent_id = request.data.get("agent_id", None)
            replay_type = request.data.get("replay_type", None)
            if replay_type is not None and int(replay_type) not in [
                const.API_REPLAY,
                const.REQUEST_REPLAY,
            ]:
                return R.failure(msg="replay_type error")
            replay_type = (
                const.REQUEST_REPLAY if replay_type is None else int(replay_type)
            )

            check_failure, method_pool_model = self.check_method_pool(
                method_pool_id, request.user
            )
            if check_failure:
                return R.failure(
                    msg=_("Stain pool data does not exist or no permission to access")
                )
            if agent_id:
                agent = IastAgent.objects.filter(pk=agent_id).first()
                check_failure = self.check_agent_active(agent)
                if check_failure and agent is not None:
                    agent = IastAgent.objects.filter(
                        bind_project_id=agent.bind_project_id, online=1
                    ).first()
                check_failure = self.check_agent_active(agent)
            else:
                check_failure = self.check_agent_active(method_pool_model.agent)
            if check_failure:
                return R.failure(
                    msg=_(
                        "The probe has been destroyed or suspended, please check the probe status"
                    )
                )

            check_failure, checked_request = self.check_replay_request(
                raw_request=replay_request
            )
            if check_failure:
                return R.failure(msg=_("Replay request is illegal"))
            if agent_id:
                replay_id = self.send_request_to_replay_queue(
                    relation_id=method_pool_model.id,
                    agent_id=agent.id,
                    replay_request=checked_request,
                    replay_type=replay_type,
                )
            else:
                replay_id = self.send_request_to_replay_queue(
                    relation_id=method_pool_model.id,
                    agent_id=method_pool_model.agent.id,
                    replay_request=checked_request,
                    replay_type=replay_type,
                )
            return R.success(
                msg=_("Relay request success"), data={"replayId": replay_id}
            )

        except Exception as e:
            print(e)
            logger.error(f"user_id:{request.user.id} msg:{e}")
            return R.failure(msg=_("Vulnerability replay error"))

    @staticmethod
    def check_replay_data_permission(replay_id, auth_agents):
        return (
            IastReplayQueue.objects.values("id")
            .filter(id=replay_id, agent__in=auth_agents)
            .exists()
        )

    @staticmethod
    def parse_response(header, body):
        try:
            _data = base64.b64decode(header.encode("utf-8")).decode("utf-8")
        except Exception as e:
            _data = ""
            logger.error(
                _("Response header analysis error, error message: {}".format(e))
            )
        return "{header}\n\n{body}".format(header=_data, body=body)

    @extend_schema_with_envcheck(
        [
            {
                "name": "replayid",
                "type": int,
                "required": True,
            },
            {
                "name": "replay_type",
                "type": int,
                "required": False,
                "description": "available options are (2,3)",
            },
        ],
        tags=["重放"],
        summary="获取请求包重放详情",
    )
    def get(self, request):
        replay_id = request.query_params.get("replayId")
        # auth_agents = self.get_auth_agents_with_user(request.user)
        replay_type = request.query_params.get("replay_type", None)
        if replay_type is not None and int(replay_type) not in [
            const.API_REPLAY,
            const.REQUEST_REPLAY,
        ]:
            return R.failure(msg="replay_type error")
        replay_type = const.REQUEST_REPLAY if replay_type is None else int(replay_type)
        replay_data = IastReplayQueue.objects.filter(id=replay_id).first()
        if not replay_data:
            return R.failure(
                status=203,
                msg=_("Replay request does not exist or no permission to access"),
            )
        if (
            request.user.is_superuser == 1
            or replay_data.agent.user_id == request.user.id
        ):
            pass
        elif (
            request.user.is_superuser == 2
            and replay_data.agent.user_id != request.user.id
        ):
            # 部门鉴权
            talent = request.user.get_talent()
            departments = talent.departments.all()
            if replay_data.agent.user.get_department() not in departments:
                replay_data = {}
        elif replay_data.agent.user_id != request.user.id:
            replay_data = {}

        if not replay_data:
            return R.failure(
                status=203,
                msg=_("Replay request does not exist or no permission to access"),
            )
        if replay_data.create_time < (int(time.time()) - 60 * 5):
            return R.failure(status=203, msg=_("重放超时"))
        if replay_data.state != const.SOLVED:
            return R.failure(msg=_("Replay request processing"))
        replay_data_method_pool = (
            IastAgentMethodPoolReplay.objects.filter(
                replay_id=replay_id, replay_type=replay_type
            )
            .values("res_header", "res_body", "method_pool", "id")
            .first()
        )
        if replay_data_method_pool:
            return R.success(
                data={
                    "response": self.parse_response(
                        replay_data_method_pool["res_header"],
                        replay_data_method_pool["res_body"],
                    ),
                    "method_pool_replay_id": replay_data_method_pool["id"],
                }
            )
        else:
            return R.failure(status=203, msg=_("Replay failed"))
