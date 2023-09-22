import logging

from django.forms.models import model_to_dict
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.project import IastProject
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer

logger = logging.getLogger("django")


class _ProjectSearchQuerySerializer(serializers.Serializer):
    name = serializers.CharField(help_text=_("Project name, support fuzzy search."))


class _ProjectSearchDataSerializer(serializers.Serializer):
    id = serializers.IntegerField(help_text=_("The id of the project"))
    name = serializers.CharField(help_text=_("The name of project"))

    class Meta:
        model = IastProject
        fields = ["id", "name"]


_ProjectResponseSerializer = get_response_serializer(_ProjectSearchDataSerializer(many=True))


class ProjectSearch(UserEndPoint):
    @extend_schema_with_envcheck(
        [_ProjectSearchQuerySerializer],
        tags=[_("Project")],
        summary=_("Projects Search"),
        description=_(
            "Get the id and name of the item according to the search keyword matching the item name, in descending order of time."
        ),
        response_schema=_ProjectResponseSerializer,
    )
    def get(self, request):
        name = request.query_params.get("name", "")
        projects = request.user.get_projects().filter(name__icontains=name).order_by("-latest_time")
        data = [model_to_dict(project, fields=["id", "name"]) for project in projects]
        return R.success(data=data)
