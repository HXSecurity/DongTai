######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : api_route_cover_rate
# @created     : Friday Aug 20, 2021 16:20:10 CST
#
# @description :
######################################################################

from dongtai_web.base.project_version import get_project_version, get_project_version_by_id
from dongtai_common.models.agent import IastAgent
from dongtai_common.endpoint import R, UserEndPoint
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from dongtai_web.utils import batch_queryset, checkcover_batch
from dongtai_web.utils import extend_schema_with_envcheck
from dongtai_common.models.api_route import IastApiRoute, FromWhereChoices
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer
from rest_framework import serializers
from dongtai_common.models.project import IastProject
import logging

logger = logging.getLogger("dongtai-webapi")


class ApiRouteCoverRateResponseSerializer(serializers.Serializer):
    cover_rate = serializers.IntegerField(
        help_text=_("The api cover_rate of the project"), )
    total_count = serializers.IntegerField(
        help_text=_("The api cover_rate of the project"), )
    cover_count = serializers.IntegerField(
        help_text=_("The coverd api number  of the project"), )


_GetResponseSerializer = get_response_serializer(
    ApiRouteCoverRateResponseSerializer())


class ApiRouteCoverRate(UserEndPoint):

    @extend_schema_with_envcheck(
        [{
            'name': 'project_id',
            'type': int
        }, {
            'name': 'version_id',
            'type': int
        }],
        tags=[_('API Route')],
        summary=_('API Route Coverrate'),
        description=_("Get the API route coverrate of the project corresponding to the specified id."),
        response_schema=_GetResponseSerializer,
    )
    def get(self, request):
        project_id = request.query_params.get('project_id', None)
        version_id = request.query_params.get('version_id', None)
        auth_users = self.get_auth_users(request.user)
        if not version_id:
            current_project_version = get_project_version(project_id)
        else:
            current_project_version = get_project_version_by_id(version_id)
        departments = request.user.get_relative_department()
        projectexist = IastProject.objects.filter(department__in=departments,
                                                  pk=project_id).first()
        if not projectexist:
            return R.failure(_("Parameter error"))
        total_count = IastApiRoute.objects.filter(
            project_id=project_id,
            project_version_id=current_project_version.get("version_id",
                                                           0)).count()
        covered_count = IastApiRoute.objects.filter(
            project_id=project_id,
            project_version_id=current_project_version.get("version_id", 0),
            is_cover=1).count()
        try:
            cover_rate = "{:.2%}".format(covered_count / total_count)
        except ZeroDivisionError as e:
            logger.info(e, exc_info=True)
            cover_rate = "{:.2%}".format(1.0)

        return R.success(
            msg=_('API coverage rate obtained successfully'),
            data={
                'cover_rate': cover_rate,
                "total_count": total_count,
                "covered_count": covered_count,
            },
        )
