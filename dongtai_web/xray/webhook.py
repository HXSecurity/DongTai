import logging
import json

from django.utils.translation import gettext_lazy as _
from dongtai_common.endpoint import AnonymousAuthEndPoint, R
from rest_framework.viewsets import ViewSet

logger = logging.getLogger('dongtai-webapi')

PLUGIN_VULTYPE_DICT = {
}

def get_iast_vul_code(plugin_str: str) -> str:
    if plugin_str.startswith("path-traversal"):
        return "path-traversal"
    if plugin_str.startswith("xss"):
        return "reflected-xss"
    if plugin_str.startswith("sqldet"):
        return "sql-injection"
    if plugin_str.startswith("cmd-injection"):
        return "cmd-injection"
    if plugin_str.startswith("brute-force"):
        return ""
    if plugin_str.startswith("redirect"):
        return "unvalidated-redirect"
#    if plugin_str.startswith("path-traversal"):
#        return "sql-injection"

    return ""

def parse_xray_uuid(response: str) -> str:
    res_list = response.split("\r\n")
    for line in res_list:
        if line.startswith("Xray"):
            key_tuple = line.split(":")
            return key_tuple[1].strip()
    return ""


def parse_agent_id(response: str) -> str:
    res_list = response.split("\r\n")
    for line in res_list:
        if line.startswith("Xray"):
            key_tuple = line.split(":")
            return key_tuple[1].strip()
    return ""


class XrayWebhook(AnonymousAuthEndPoint):
    name = "api-v1-xray-webhook"
    description = _("Xray Webhook")

    def post(self, request):
        if "type" in request.data and request.data["type"] == "web_statistic":
            logger.debug(request.data)
        elif "type" in request.data and request.data["type"] == "web_vuln":
            for reqres_pair in request.data['detail']['snapshot']:
                req, res = reqres_pair
                header = parse_res_header(res)
        return R.success()
