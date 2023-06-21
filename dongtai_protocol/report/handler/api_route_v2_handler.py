######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : api_route_handler
# @created     : Tuesday Aug 17, 2021 19:59:29 CST
#
# @description :
######################################################################

from dongtai_protocol.report.handler.report_handler_interface import IReportHandler
from dongtai_protocol.report.report_handler_factory import ReportHandler
from dongtai_common.models.api_route_v2 import IastApiRouteV2, FromWhereChoices
from dongtai_common.models.agent import IastAgent
from dongtai_common.utils import const
import logging
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from dongtai_common.models.project import IastProject
from dongtai_engine.plugins.project_time_update import project_time_stamp_update
from celery import shared_task
import re

logger = logging.getLogger('dongtai.openapi')


@ReportHandler.register(const.REPORT_API_ROUTE_V2)
class ApiRouteV2Handler(IReportHandler):

    def parse(self):
        self.api_data = self.detail.get('apiData')

    def save(self):
        api_route_gather_v2.delay(self.agent_id, self.api_data)


def find_values_with_key(dictionary, key):
    values = []
    for dic_key, value in dictionary.items():
        if isinstance(value, dict):
            values.extend(find_values_with_key(value, key))
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    values.extend(find_values_with_key(item, key))
        if key == dic_key:
            values.append(value)
    return values


def get_schama_key(ref_str: str) -> str:
    return ref_str.replace("#/components/schemas/", "")


def validate_schema_key(test_str: str) -> bool:
    return re.fullmatch(r"#\/components\/schemas\/.*", test_str) is not None


@shared_task(queue='dongtai-api-route-handler')
def api_route_gather_v2(agent_id, api_routes):
    logger.info(_('API navigation log start '), )
    try:
        agent = IastAgent.objects.get(pk=agent_id)

        schemas = api_routes['components']['schemas']

        api_routes_list = []
        for path, path_info in api_routes['paths'].items():
            for method, api in path_info.items():
                ref_in_api = find_values_with_key(api, '$ref')
                schema_keys = [get_schama_key(i) for i in ref_in_api]
                extenal_schema_keys = []
                for key in schema_keys:
                    extenal_schema_keys.extend(
                        find_values_with_key(schemas[key], "$ref"))
                extenal_schema_keys = [
                    get_schama_key(i) for i in extenal_schema_keys
                ]
                keys = set(schema_keys + extenal_schema_keys)
                new_dict = {
                    "paths": {
                        path: {
                            method: api
                        }
                    },
                    "components": {
                        "schemas": {key: schemas[key]
                                    for key in keys}
                    }
                }
                api_route = IastApiRouteV2(
                    path=path,
                    method=method,
                    from_where=FromWhereChoices.FROM_AGENT,
                    project_id=agent.bind_project_id,
                    project_version_id=agent.project_version_id,
                    api_info=new_dict,
                )
                api_routes_list.append(api_route)
        IastApiRouteV2.objects.bulk_create(api_routes_list,
                                           ignore_conflicts=False)
    except Exception as e:
        logger.info(
            _('API navigation log failed, why: {}').format(e),
            exc_info=e,
        )
