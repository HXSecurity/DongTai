######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : api_route_handler
# @created     : Tuesday Aug 17, 2021 19:59:29 CST
#
# @description :
######################################################################

from dongtai_protocol.report.handler.report_handler_interface import IReportHandler
from dongtai_protocol.report.report_handler_factory import ReportHandler
from dongtai_common.models.api_route import IastApiRoute, IastApiMethod, \
    IastApiResponse, IastApiParameter, \
    IastApiMethodHttpMethodRelation, HttpMethod
from dongtai_common.models.agent import IastAgent
from dongtai_common.utils import const
import logging
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from dongtai_common.models.project import IastProject
from dongtai_engine.plugins.project_time_update import (
    project_time_stamp_update,
    project_version_time_stamp_update,
)
from celery import shared_task

logger = logging.getLogger('dongtai.openapi')


@ReportHandler.register(const.REPORT_API_ROUTE)
class ApiRouteHandler(IReportHandler):

    def parse(self):
        self.api_data = self.detail.get('apiData')
        self.api_routes = list(map(lambda x: _data_dump(x), self.api_data))

    def save(self):
        api_route_gather.delay(self.agent_id, self.api_routes)


@shared_task(queue='dongtai-api-route-handler')
def api_route_gather(agent_id, api_routes):
    try:
        agent = IastAgent.objects.filter(pk=agent_id)[0:1]
        if not agent:
            raise ValueError(_("No such agent"))
        agent = agent[0]
        for api_route in api_routes:
            logger.debug(f"recoding api_route: {api_route}")
            http_methods = []
            with transaction.atomic():
                try:
                    for http_method_str in api_route['method']:
                        http_method, __ = HttpMethod.objects.get_or_create(
                            method=http_method_str.upper())
                        http_methods.append(http_method)
                        api_method, is_create = IastApiMethod.objects.get_or_create(
                            method=http_method_str.upper())
                        if is_create:
                            for http_method in http_methods:
                                IastApiMethodHttpMethodRelation.objects.create(
                                    api_method_id=api_method.id,
                                    http_method_id=http_method.id)
                        fields = [
                            'uri', 'code_class', 'description', 'code_file',
                            'controller', 'agent'
                        ]
                        api_route_dict = _dictfilter(api_route, fields)
                        api_route_obj = _route_dump(api_route_dict, api_method,
                                                    agent)
                        api_route_model, is_create = IastApiRoute.objects.get_or_create(
                            **api_route_obj)
                        parameters = api_route['parameters']
                        for parameter in parameters:
                            parameter_obj = _para_dump(parameter,
                                                       api_route_model)
                            IastApiParameter.objects.get_or_create(
                                **parameter_obj)
                        response_obj = _response_dump(
                            {'return_type': api_route['returnType']},
                            api_route_model)
                        IastApiResponse.objects.get_or_create(**response_obj)
                except Exception as e:
                    print(e)
            logger.info(_('API navigation log record successfully'))
        project_time_stamp_update.apply_async((agent.bind_project_id, ),
                                              countdown=5)
        project_version_time_stamp_update.apply_async(
            (agent.project_version_id, ), countdown=5)
    except Exception as e:
        logger.info(_('API navigation log failed, why: {}').format(e),
                    exc_info=e)


def _data_dump(item):
    item['code_class'] = item['class']
    item['code_file'] = item['file']
    return item


def _route_dump(item, api_method, agent):
    item['method'] = api_method
    item['agent'] = agent
    item['path'] = item['uri']
    del item['uri']
    item['project_id'] = agent.bind_project_id
    item['project_version_id'] = agent.project_version_id
    return item


def _para_dump(item, api_route):
    item = item.copy()
    item['route'] = api_route
    item['parameter_type'] = item['type']
    del item['type']
    return item


def _response_dump(item, api_route):
    item = item.copy()
    item['route'] = api_route
    return item


def _dictfilter(dict_: dict, fields: list):
    return {k: v for k, v in dict_.items() if k in fields}
