#!/usr/bin/env python
# datetime: 2021/4/27 下午2:48

import json
import logging
import time

import re2 as re
from django.db import IntegrityError

from dongtai_common.models.agent import IastAgent
from dongtai_common.models.header_vulnerablity import IastHeaderVulnerability
from dongtai_common.models.hook_type import HookType
from dongtai_common.models.project import IastProject
from dongtai_common.models.strategy import IastStrategyModel
from dongtai_common.models.vulnerablity import IastVulnerabilityModel
from dongtai_common.utils import const
from dongtai_conf import settings
from dongtai_engine.signals import send_notify
from dongtai_protocol import utils
from dongtai_protocol.report.handler.report_handler_interface import IReportHandler
from dongtai_protocol.report.report_handler_factory import ReportHandler
from dongtai_web.vul_log.vul_log import log_vul_found

logger = logging.getLogger("dongtai.openapi")


class BaseVulnHandler(IReportHandler):
    def __init__(self):
        super().__init__()
        self.app_name = None
        self.http_uri = None
        self.http_url = None
        self.http_query_string = None
        self.http_header = None
        self.http_method = None
        self.http_scheme = None
        self.http_secure = None
        self.http_protocol = None
        self.vuln_type = None
        self.app_caller = None
        self.taint_value = None
        self.client_ip = None

    @staticmethod
    def create_top_stack(obj):
        return f'{obj["classname"]}.{obj["methodname"]}({obj["in"]})'

    @staticmethod
    def create_bottom_stack(obj):
        return f'{obj["classname"]}.{obj["methodname"]}("{obj["in"]}")'

    def get_vul_info(self):
        level_id = 0
        vul_type = self.vuln_type
        vul_type_enable = "disable"
        hook_type_id = 0
        strategy_id = 0
        # 根据用户ID判断获取策略中的漏洞等级
        hook_type = HookType.objects.values("id", "enable").filter(value=vul_type).first()
        if hook_type:
            hook_type_id = hook_type.get("id", 0)
            vul_type_enable = hook_type.get("enable", 0)
            strategy = IastStrategyModel.objects.values("level_id", "id").filter(hook_type_id=hook_type_id).first()
            if strategy:
                level_id = strategy.get("level_id", 4)
                strategy_id = strategy.get("id", 0)

        return level_id, vul_type, vul_type_enable, hook_type_id, strategy_id

    @staticmethod
    def get_command(envs):
        for env in envs:
            if "sun.java.command" in env.lower():
                return "=".join(env.split("=")[1:])
        return ""

    @staticmethod
    def get_runtime(envs):
        for env in envs:
            if "java.runtime.name" in env.lower():
                return "=".join(env.split("=")[1:])
        return ""

    def parse(self):
        self.server_name = self.detail.get("serverName")
        self.server_port = self.detail.get("serverPort")
        self.server_env = self.detail.get("serverEnv")
        self.hostname = self.detail.get("hostname")
        self.agent_version = self.detail.get("agentVersion")
        self.app_name = self.detail.get("appName")
        self.app_path = self.detail.get("contextPath")
        self.http_uri = self.detail.get("uri")
        self.http_url = self.detail.get("url")
        self.http_query_string = self.detail.get("queryString")
        self.http_header = self.detail.get("reqHeader")
        self.http_req_data = self.detail.get("reqBody")
        self.http_method = self.detail.get("method")
        self.http_scheme = self.detail.get("scheme")
        self.http_secure = self.detail.get("secure")
        self.http_protocol = self.detail.get("protocol")
        self.vuln_type = self.detail.get("vulnType")
        self.app_caller = self.detail.get("appCaller")
        self.taint_value = self.detail.get("taintValue")
        self.taint_position = self.detail.get("taintPosition")
        self.client_ip = self.detail.get("clientIp")
        self.param_name = self.detail.get("paramName")
        self.container = self.detail.get("container")
        self.container_path = self.detail.get("containerPath")
        self.http_replay = self.detail.get("replayRequest")
        self.http_res_header = self.detail.get("resHeader")
        self.http_res_body = self.detail.get("resBody")
        self.req_header_for_search = utils.build_request_header(
            req_method=self.http_method,
            raw_req_header=self.http_header,
            uri=self.http_uri,
            query_params=self.http_query_string,
            http_protocol=self.http_protocol,
        )


@ReportHandler.register(const.REPORT_VULN_NORNAL)
class NormalVulnHandler(BaseVulnHandler):
    def save(self):
        logger.info("NormalVulnHandler start")
        logger.info(f"vuln_type: {self.vuln_type} vuln_type: {self.http_uri} agent_id: {self.agent_id}")
        if self.http_replay:
            return

        (
            level_id,
            vul_type,
            vul_type_enable,
            hook_type_id,
            strategy_id,
        ) = self.get_vul_info()
        logger.info("get_vul_info start")
        logger.info(f"{level_id} {vul_type} {vul_type_enable} {hook_type_id} {strategy_id}")
        index = -1
        if vul_type_enable == 0:
            return
        caller_message = self.app_caller[index + 2]
        sink_message = self.app_caller[index + 1]
        caller_message_location = re.search("\\(.*\\)", caller_message).group(0).strip("()").split(":")
        if len(caller_message_location) == 2:
            caller_message_file, caller_message_linenumber = caller_message_location
        else:
            caller_message_location[0]
            caller_message_linenumber = 0
        full_stack = [
            [
                {
                    "args": "",
                    "source": False,
                    "invokeId": 1,
                    "className": ".".join(re.search(".*\\(", sink_message).group(0).strip("()").split(".")[:-1]),
                    "signature": sink_message,
                    "interfaces": [],
                    "methodName": re.search(".*\\(", sink_message).group(0).strip("()").split(".")[-1],
                    "sourceHash": [],
                    "targetHash": [],
                    "callerClass": ".".join(re.search(".*\\(", caller_message).group(0).strip("()").split(".")[:-1]),
                    "targetRange": [],
                    "callerMethod": re.search(".*\\(", caller_message).group(0).strip("()").split(".")[-1],
                    "retClassName": "",
                    "sourceValues": "",
                    "targetValues": "",
                    "originClassName": ".".join(re.search(".*\\(", sink_message).group(0).strip("()").split(".")[:-1]),
                    "callerLineNumber": caller_message_linenumber,
                    "sourceHashForRpc": [],
                    "targetHashForRpc": [],
                    "sourceIsReference": False,
                    "targetIsReference": False,
                    "projectPropagatorClose": False,
                    "tag": "sink",
                    "code": sink_message,
                    "stack": self.app_caller,
                }
            ]
        ]
        IastAgent.objects.filter(project_version_id=self.agent.project_version_id)
        iast_vul = (
            IastVulnerabilityModel.objects.filter(
                strategy_id=strategy_id,
                uri=self.app_caller[index + 2],
                http_method="",
                project_version_id=self.agent.project_version_id,
                is_del=0,
            )
            .order_by("-latest_time")
            .first()
        )
        project = IastProject.objects.filter(pk=self.agent.bind_project_id).first()
        from dongtai_common.models.strategy_user import IastStrategyUser

        scan_template = IastStrategyUser.objects.filter(pk=project.scan_id).first()
        if scan_template:
            strategy_ids = [int(i) for i in scan_template.content.split(",")]
            if strategy_id not in strategy_ids:
                return
        if project:
            project.update_latest()
        timestamp = int(time.time())
        if iast_vul:
            iast_vul.uri = self.app_caller[index + 2]
            iast_vul.url = self.app_caller[index + 2]
            iast_vul.req_header = self.http_header
            iast_vul.req_params = self.http_query_string
            iast_vul.res_header = self.http_res_header
            iast_vul.res_body = self.http_res_body
            iast_vul.full_stack = json.dumps(full_stack, ensure_ascii=False)
            iast_vul.top_stack = self.app_caller[index + 1]
            iast_vul.bottom_stack = self.app_caller[index + 2]
            iast_vul.counts = iast_vul.counts + 1
            iast_vul.latest_time = timestamp
            iast_vul.status_id = settings.CONFIRMED
            iast_vul.save()
        else:
            iast_vul = IastVulnerabilityModel.objects.create(
                strategy_id=strategy_id,
                hook_type_id=hook_type_id,
                level_id=level_id,
                url=self.app_caller[index + 2],
                uri=self.app_caller[index + 2],
                http_method="",
                http_scheme=self.http_scheme,
                http_protocol=self.http_protocol,
                req_header=self.http_header,
                req_params=self.http_query_string,
                req_data=self.http_req_data,
                res_header=self.http_res_header,
                res_body=self.http_res_body,
                agent=self.agent,
                context_path=self.app_path,
                counts=1,
                status_id=settings.CONFIRMED,
                first_time=timestamp,
                latest_time=timestamp,
                client_ip=self.client_ip,
                full_stack=json.dumps(full_stack, ensure_ascii=False),
                top_stack=self.app_caller[index + 1],
                bottom_stack=self.app_caller[index + 2],
                project_version_id=self.agent.project_version_id,
                project_id=self.agent.bind_project_id,
                language=self.agent.language,
                server_id=self.agent.server_id,
            )
            log_vul_found(
                iast_vul.agent.user_id,
                iast_vul.agent.bind_project.name,
                iast_vul.agent.bind_project_id,
                iast_vul.id,  # type: ignore
                iast_vul.strategy.vul_name,
            )
            send_notify.send_robust(sender=self.__class__, vul_id=iast_vul.id)

        IastVulnerabilityModel.objects.filter(
            strategy_id=iast_vul.strategy_id,
            uri=iast_vul.uri,
            http_method=iast_vul.http_method,
            project_version_id=iast_vul.agent.project_version_id,
            pk__lt=iast_vul.id,
        ).delete()
        if not IastHeaderVulnerability.objects.filter(
            project_id=self.agent.bind_project_id,
            project_version_id=self.agent.project_version_id,
            url=self.http_uri,
            vul=iast_vul.id,
        ).exists():
            try:
                IastHeaderVulnerability.objects.create(
                    project_id=self.agent.bind_project_id,
                    project_version_id=self.agent.project_version_id,
                    url=self.http_uri,
                    vul_id=iast_vul.id,
                )
            except IntegrityError:
                logger.debug("unique error stack: ", exc_info=True)
                logger.info("unique error cause by concurrency insert,ignore it")
        # disable when no req_header and res_header


#        if header_vul and not IastHeaderVulnerabilityDetail.objects.filter(
#        ).exists():
#                IastHeaderVulnerabilityDetail.objects.create(
#                    res_header=self.http_res_header)
#                logger.info(
#                    "unique error cause by concurrency insert,ignore it")
