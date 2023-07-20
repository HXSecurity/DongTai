from rest_framework import serializers
from dongtai_common.models.asset_vul_v2 import IastAssetVulV2


class PackageVulSerializer(serializers.ModelSerializer):
    level_name = serializers.CharField(source="get_level_display")
    level_id = serializers.IntegerField(source="level")

    class Meta:
        model = IastAssetVulV2
        fields = "__all__"
