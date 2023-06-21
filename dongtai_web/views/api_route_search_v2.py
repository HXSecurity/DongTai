import logging
import time
from dongtai_common.endpoint import R
from django.db.models import Q
from django.forms.models import model_to_dict
from dongtai_common.endpoint import UserEndPoint
from dongtai_common.models.project_version import IastProjectVersion
from dongtai_common.models.api_route_v2 import IastApiRouteV2
from django.utils.translation import gettext_lazy as _
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from dongtai_common.serializers.api_route_v2 import ApiRouteV2DetailSerializer


class ApiRouteArgSerializer(serializers.Serializer):
    page_size = serializers.IntegerField(default=20,
                                         help_text=_('Number per page'))
    page = serializers.IntegerField(default=1, help_text=_('Page index'))
    version_id = serializers.IntegerField(default=None,
                                          help_text=_('Project id'),
                                          required=False)
    project_id = serializers.IntegerField(default=None,
                                          help_text=_('Project id'),
                                          required=False)
    is_cover = serializers.IntegerField(default=None,
                                        help_text=_('Project id'),
                                        required=False)
    from_where = serializers.IntegerField(default=None,
                                          help_text=_('Project id'),
                                          required=False)
    uri = serializers.CharField(help_text=_("The uri of the api route"),
                                required=False)
    http_method = serializers.CharField(
        help_text=_("The http method of the api route"), required=False)


class NewApiRouteV2Search(UserEndPoint):
    name = "api-v1-api-route-search"
    description = _("Delete application version information")

    @extend_schema_with_envcheck(
        request=ApiRouteArgSerializer,
        tags=[_('API Route')],
        summary=_('New api route search v3'),
        description=
        _("Get the item corresponding to the user, support fuzzy search based on name."
          ),
    )
    def post(self, request):
        ser = ApiRouteArgSerializer(data=request.data)
        try:
            if ser.is_valid(True):
                page_size = ser.validated_data['page_size']
                page = ser.validated_data['page']
                project_id = ser.validated_data['project_id']
                version_id = ser.validated_data['version_id']
                is_cover = ser.validated_data['is_cover']
                from_where = ser.validated_data['from_where']
        except ValidationError as e:
            return R.failure(data=e.detail)
        q = Q()
        if project_id:
            q = q & Q(project_id=project_id)
        if version_id:
            q = q & Q(project_version_id=version_id)
        if is_cover is not None:
            q = q & Q(is_cover=is_cover)
        if from_where is not None:
            q = q & Q(from_where=from_where)
        if 'http_method' in ser.validated_data and ser.validated_data[
                'http_method']:
            q = q & Q(method=ser.validated_data['http_method'])
        if 'uri' in ser.validated_data and ser.validated_data['uri']:
            q = q & Q(uri=ser.validated_data['uri'])
        api_routes = IastApiRouteV2.objects.filter(q).order_by('-id')
        page_info, data = self.get_paginator(api_routes, page, page_size)
        return R.success(data=ApiRouteV2DetailSerializer(data, many=True).data,
                         page=page_info)
