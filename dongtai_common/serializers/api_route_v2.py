from rest_framework import serializers
from dongtai_common.models.api_route_v2 import IastApiRouteV2
from dongtai_common.models.vulnerablity import IastVulnerabilityModel
from django.db.models import QuerySet, F


def _get_vuls(uri, project_version_id):
    vuls = IastVulnerabilityModel.objects.filter(
        uri=uri, project_version_id=project_version_id,
        is_del=0).annotate(hook_type_name=F('strategy__vul_name')).values(
            'id', 'level_id', 'hook_type_name').distinct().all()
    return list(vuls)


class ApiRouteV2DetailSerializer(serializers.ModelSerializer):
    vulnerablities = serializers.SerializerMethodField()

    def get_vulnerablities(self, obj):
        if obj.is_cover:
            return _get_vuls(obj.path, obj.project_version_id)
        return []

    class Meta:
        model = IastApiRouteV2
        fields = [
            'id', 'path', 'method', 'from_where', 'project', 'project_version',
            'is_cover', 'api_info', 'vulnerablities'
        ]
