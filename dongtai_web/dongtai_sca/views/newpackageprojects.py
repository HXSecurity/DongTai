import logging

from dongtai_common.models import User
from dongtai_web.dongtai_sca.models import Package
from django.http import JsonResponse
from rest_framework import views
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from dongtai_common.endpoint import R, UserEndPoint
from django.utils.translation import gettext_lazy as _
from dongtai_web.utils import extend_schema_with_envcheck_v2, get_response_serializer
from rest_framework import serializers

from dongtai_web.dongtai_sca.utils import get_asset_id_by_aggr_id
from dongtai_common.models.assetv2 import AssetV2, AssetV2Global
from rest_framework_dataclasses.serializers import DataclassSerializer
from dataclasses import dataclass, field
from typing import List
from typing import Any
from dataclasses import dataclass
import json

logger = logging.getLogger(__name__)


@dataclass
class RelationProject:
    project_id: int
    project_name: str


class RelationProjectArgsSerializer(serializers.Serializer):
    page_size = serializers.IntegerField(default=20,
                                         help_text=_('Number per page'))
    page = serializers.IntegerField(default=1, help_text=_('Page index'))
    package_name = serializers.CharField(help_text=_("order_field"))
    package_version = serializers.CharField(help_text=_("order"))
    project_id = serializers.IntegerField(
        help_text=_("project with be the first"))


class RelationProjectSerializer(DataclassSerializer):

    class Meta:
        dataclass = RelationProject


FullRelationProjectResponseSerializer = get_response_serializer(
    RelationProjectSerializer(many=True))


class NewPackageRelationProject(UserEndPoint):

    @extend_schema_with_envcheck_v2(
        request=RelationProjectArgsSerializer,
        responses={200: FullRelationProjectResponseSerializer})
    def post(self, request):
        return JsonResponse({})