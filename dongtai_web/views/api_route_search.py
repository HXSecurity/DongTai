######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : api_route_search
# @created     : Wednesday Aug 18, 2021 14:31:17 CST
#
# @description :
######################################################################

from django.db.models import Q
from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.api_route import (
    IastApiRoute,
    IastApiMethod,
    HttpMethod,
)
from dongtai_common.models.agent import IastAgent
from dongtai_web.base.project_version import get_project_version, get_project_version_by_id
from dongtai_common.models.vulnerablity import IastVulnerabilityModel
from django.forms.models import model_to_dict
from functools import partial
from dongtai_common.models.hook_type import HookType
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer
import logging
from dongtai_common.models.strategy import IastStrategyModel
from dongtai_common.models.project import IastProject

logger = logging.getLogger('dongtai-webapi')


class ApiRouteSearchRequestBodySerializer(serializers.Serializer):
    page_size = serializers.IntegerField(
        help_text=_("number per page"),
        required=False,
        default=1)
    uri = serializers.CharField(help_text=_("The uri of the api route"),
                                required=False)
    http_method = serializers.CharField(
        help_text=_("The http method of the api route"), required=False)
    project_id = serializers.IntegerField(help_text=_("The id of the project"), )
    version_id = serializers.IntegerField(
        help_text=_("The version id of the project"), required=False)
    exclude_ids = serializers.CharField(help_text=_(
        "Exclude the api route entry with the following id, this field is used to obtain the data of the entire project in batches."
    ),
        required=False)
    is_cover = serializers.ChoiceField(
        (1, 0),
        help_text=_("Whether the api is covered by detection, that is, there is associated request data in the record."
                    ),
        required=False,
    )


class ApiRouteHttpMethodSerialier(serializers.Serializer):
    httpmethod = serializers.CharField()


class ApiRouteMethodSerialier(serializers.Serializer):
    apimethod = serializers.CharField(
        help_text=_("The method bound to this API"))
    httpmethods = ApiRouteHttpMethodSerialier(
        help_text=_("The method bound to this API, in array form"), many=True)


class ApiRouteParameterSerialier(serializers.Serializer):
    id = serializers.IntegerField(help_text=_("The id of api route"))
    name = serializers.CharField(help_text=_("The name of api route"))
    parameter_type = serializers.CharField(
        help_text=_("The type of the parameter"))
    parameter_type_shortcut = serializers.CharField(help_text=_(
        "The shortcut of the parameter_type,e.g. java.lang.String -> String"))
    annotaion = serializers.CharField(
        help_text=_("The annotaion of the parameter"))
    route = serializers.IntegerField(help_text=_("The route id of parameter"))


class ApiRouteResponseSerialier(serializers.Serializer):
    id = serializers.IntegerField(help_text=_("The id of api response"))
    return_type = serializers.CharField(
        help_text=_("The return type of api route"))
    route = serializers.IntegerField(
        help_text=_("The route id of api response"))
    return_type_shortcut = serializers.CharField(
        help_text=_("The shortcut of return_type"))


class ApiRouteVulnerabitySerialier(serializers.Serializer):
    level_id = serializers.IntegerField(
        help_text=_("The vulnerablity level id "))
    hook_type_name = serializers.CharField(
        help_text=_("The vulnerablity type name"))


class ApiRouteSearchResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField(help_text=_("The id of api route"))
    path = serializers.CharField(help_text=_("The uri of api route"))
    code_class = serializers.CharField(help_text=_("The class of api route"))
    description = serializers.CharField(
        help_text=_("The description of the api route"))
    code_file = serializers.CharField(
        help_text=_("The code file of the api route"))
    controller = serializers.CharField(
        help_text=_("The controller of the api route"))
    agent = serializers.IntegerField(
        help_text=_("The id of the agent reported the api route"))
    is_cover = serializers.ChoiceField(
        (1, 0),
        help_text=_("Whether the api is covered by detection, that is, there is associated request data in the record."
                    ),
        required=False,
    )
    responses = ApiRouteResponseSerialier(many=True)
    parameters = ApiRouteParameterSerialier(many=True)
    vulnerablities = ApiRouteVulnerabitySerialier(many=True)
    method = ApiRouteMethodSerialier()


_GetResponseSerializer = get_response_serializer(
    ApiRouteSearchResponseSerializer())


class ApiRouteSearch(UserEndPoint):
    @extend_schema_with_envcheck(
        request=ApiRouteSearchRequestBodySerializer,
        tags=[_('API Route')],
        summary=_('API Route Search'),
        description=_("Get the API list corresponding to the project according to the following parameters. By default, there is no sorting. Please use the exclude_ids field for pagination."
                      ),
        response_schema=_GetResponseSerializer,
    )
    def post(self, request):
        try:
            page_size = int(request.data.get('page_size', 1))
            page_index = int(request.data.get('page_index', 0))
            uri = request.data.get('uri', None)
            http_method = request.data.get('http_method', None)
            project_id = request.data.get('project_id', None)
            project_id = int(project_id) if project_id else None
            version_id = request.data.get('version_id', None)
            version_id = int(version_id) if version_id else None
            exclude_id = request.data.get('exclude_ids', None)
            exclude_id = [int(i)
                          for i in exclude_id.split(',')] if exclude_id else None
            is_cover = request.data.get('is_cover', None)
            is_cover_dict = {1: True, 0: False}
            is_cover = is_cover_dict[int(is_cover)] if is_cover is not None and is_cover != '' else None
        except Exception as e:
            logger.error(e)
            return R.failure(_("Parameter error"))
        auth_users = self.get_auth_users(request.user)

        if http_method:
            http_method_obj = HttpMethod.objects.filter(method=http_method.upper())[0:1]
            if http_method_obj:
                api_methods = IastApiMethod.objects.filter(
                    http_method__id=http_method_obj[0].id).all().values('id')
            else:
                api_methods = []
        else:
            api_methods = []

        if not version_id:
            current_project_version = get_project_version(
                project_id)
        else:
            current_project_version = get_project_version_by_id(version_id)
        departments = request.user.get_relative_department()
        agents = IastAgent.objects.filter(
            bind_project__department__in=departments,
            bind_project_id=project_id,
            project_version_id=current_project_version.get("version_id",
                                                           0)).values("id")
        q = Q(agent_id__in=[_['id'] for _ in agents])
        projectexist = IastProject.objects.filter(department__in=departments,
                                                  pk=project_id).first()
        if not projectexist:
            return R.failure(_("Parameter error"))
        agents = IastAgent.objects.filter(
            bind_project_id=project_id,
            project_version_id=current_project_version.get("version_id",
                                                           0)).values("id")
        q = Q(project_version_id=current_project_version.get("version_id", 0),
              project_id=project_id)
        q = q & Q(
            method_id__in=[_['id']
                           for _ in api_methods]) if api_methods != [] else q
        q = q & Q(path__icontains=uri) if uri else q
        q = q & ~Q(pk__in=exclude_id) if exclude_id and not page_index else q
        q = q & Q(is_cover=is_cover) if is_cover is not None else q
        api_routes = IastApiRoute.objects.filter(q).order_by(
            'id').select_related('method').prefetch_related(
                'iastapiresponse_set', 'iastapiparameter_set').all()
        if page_index:
            no_used, api_routes = self.get_paginator(api_routes, page_index,
                                                     page_size)
        distinct_fields = ["path", "method_id"]
        distinct_exist_list = [] if not exclude_id else list(
            set(
                filter(lambda x: x != '', [
                    distinct_key(
                        IastApiRoute.objects.filter(pk=i).values(
                            "path", "method_id").first(), distinct_fields)
                    for i in exclude_id
                ])))
        _filter_and_label_partial = partial(
            _filter_and_label,
            distinct=True,
            distinct_fields=distinct_fields,
            distinct_exist_list=distinct_exist_list)
        api_routes = _filter_and_label_partial(
            api_routes, page_size, agents, http_method,
            is_cover) if is_cover is not None else _filter_and_label_partial(
                api_routes, page_size, agents, http_method)
        return R.success(
            data=[_serialize(api_route, agents) for api_route in api_routes])


def _filter_and_label(api_routes,
                      limit,
                      agents,
                      http_method,
                      is_cover=None,
                      distinct=True,
                      distinct_fields=['path', 'method_id'],
                      distinct_exist_list=[]):
    api_routes_after_filter = []
    distinct_exist_list = distinct_exist_list.copy()
    for api_route in api_routes:
        distinct_key_ = distinct_key(
            {
                'path': api_route.path,
                'method_id': api_route.method.id
            }, distinct_fields)
        if distinct_key_ in distinct_exist_list:
            continue
        else:
            distinct_exist_list.append(distinct_key_)
#        api_route.is_cover = checkcover(api_route, agents, http_method)
        if is_cover is not None:
            api_routes_after_filter += [
                api_route
            ] if api_route.is_cover == is_cover else []
        else:
            api_routes_after_filter += [api_route]
        if limit == len(api_routes_after_filter):
            break
    return api_routes_after_filter


def distinct_key(objects, fields):
    if objects is None:
        return ''
    sequence = [objects.get(field, 'None') for field in fields]
    sequence = [
        item if isinstance(item, str) else str(item) for item in sequence
    ]
    return '_'.join(sequence)


def _serialize(api_route, agents):
    item = model_to_dict(api_route)
    is_cover_dict = {1: True, 0: False}
    is_cover_dict = _inverse_dict(is_cover_dict)
    item['is_cover'] = is_cover_dict[api_route.is_cover]
    item['parameters'] = _get_parameters(api_route)
    item['responses'] = _get_responses(api_route)
    item['method'] = _get_api_method(api_route.method)
    item['vulnerablities'] = _get_vuls(item['path'], agents)
    return item


def serialize(api_route):
    item = model_to_dict(api_route)
    item['parameters'] = _get_parameters(api_route)
    item['responses'] = _get_responses(api_route)
    item['method'] = _get_api_method(item['method'])
    return item


def _get_vuls(uri, agents):
    vuls = IastVulnerabilityModel.objects.filter(
        uri=uri, agent_id__in=[_['id'] for _ in agents],
        is_del=0).values('hook_type_id', 'level_id', 'strategy_id',
                         'strategy__vul_name').distinct().all()
    return [_get_hook_type(dict(vul)) for vul in vuls]


def _get_hook_type(vul: dict) -> dict:
    return {
        'hook_type_name': vul['strategy__vul_name'],
        'level_id': vul['level_id']
    }

    hook_type = HookType.objects.filter(pk=vul['hook_type_id']).first()
    hook_type_name = hook_type.name if hook_type else None
    strategy = IastStrategyModel.objects.filter(pk=vul['strategy_id']).first()
    strategy_name = strategy.vul_name if strategy else None
    type_ = list(
        filter(lambda x: x is not None, [strategy_name, hook_type_name]))
    type_name = type_[0] if type_ else ''
    return {'hook_type_name': type_name, 'level_id': vul['level_id']}


def _get_parameters(api_route):
    parameters = api_route.iastapiparameter_set.all()
    #    parameters = IastApiParameter.objects.filter(route=api_route).all()
    parameters = [model_to_dict(parameter) for parameter in parameters]
    parameters = [_get_parameters_type(parameter) for parameter in parameters]
    return parameters


def _get_parameters_type(api_route):
    api_route['parameter_type_shortcut'] = api_route['parameter_type'].split(
        '.')[-1]
    return api_route


def _get_responses(api_route):
    responses = api_route.iastapiresponse_set.all()
    #    responses = IastApiResponse.objects.filter(route=api_route).all()
    responses = [model_to_dict(response) for response in responses]
    responses = [_get_responses_type(response) for response in responses]
    return responses


def _get_responses_type(api_route):
    api_route['return_type_shortcut'] = api_route['return_type'].split('.')[-1]
    return api_route


def _get_api_method(api_method):
    apimethod = api_method.http_method.all()
    res = {}
    res['apimethod'] = api_method.method
    res['httpmethods'] = [_.method for _ in api_method.http_method.all()]
    return res
#    if apimethod:
#        res = {}
#        res['apimethod'] = apimethod.method
#        res['httpmethods'] = [_.method for _ in apimethod.http_method.all()]
#        return res
#    return {}


def _inverse_dict(dic: dict) -> dict:
    return {v: k for k, v in dic.items()}
