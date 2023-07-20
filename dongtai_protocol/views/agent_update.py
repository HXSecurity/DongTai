import logging
import time

from dongtai_common.models.agent import IastAgent
from dongtai_common.endpoint import OpenApiEndPoint, R
from dongtai_protocol.decrypter import parse_data
from drf_spectacular.utils import extend_schema
from dongtai_common.models.server import IastServer
from django.utils.translation import gettext_lazy as _
from urllib.parse import urlparse, urlunparse
from dongtai_web.views.project_add import is_ip
from dongtai_common.utils.const import OPERATE_PUT

logger = logging.getLogger("dongtai.openapi")


class AgentUpdateEndPoint(OpenApiEndPoint):
    @extend_schema(
        summary="agent配置",
        tags=["Agent服务端交互协议", OPERATE_PUT],
        deprecated=True,
        description="Agent Update, Data is Gzip",
        responses=[{204: None}],
        methods=["POST"],
    )
    def post(self, request):
        try:
            param = parse_data(request.read())
            agent_id = int(param.get("agentId", None))
            server_addr = param.get("serverAddr", None)
            server_port = int(param.get("serverPort", None))
            protocol = param.get("protocol", "")
        except Exception as e:
            logger.error(e, exc_info=True)
            return R.failure(msg="参数错误")
        logger.info(f"agent_id:{agent_id} update_fields:{param}")
        ip = ""
        parse_re = urlparse(server_addr)
        if parse_re.hostname and is_ip(parse_re.hostname):
            ip = parse_re.hostname
        user = request.user
        agent = IastAgent.objects.filter(id=agent_id, user=user).first()
        if not agent:
            return R.failure(msg="agent no register")
        server = IastServer.objects.filter(id=agent.server_id).first()
        if not server:
            return R.failure(msg="agent no register")
        update_fields = ["port", "update_time"]
        if protocol:
            server.protocol = protocol
            update_fields.append("protocol")
        if ip:
            server.ip = ip
            update_fields.append("ip")
        server.port = server_port
        server.update_time = int(time.time())
        server.save(update_fields=update_fields)
        logger.info(_("Server record update success"))
        return R.success(msg="success update")
