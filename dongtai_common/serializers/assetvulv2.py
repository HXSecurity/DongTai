from rest_framework import serializers

from dongtai_common.models.asset_vul_v2 import IastAssetVulV2
from dongtai_web.dongtai_sca.scan.utils import get_sca_language_profile


class PackageVulSerializer(serializers.ModelSerializer):
    vul_name = serializers.SerializerMethodField()
    vul_detail = serializers.SerializerMethodField()
    level_name = serializers.CharField(source="get_level_display")
    level_id = serializers.IntegerField(source="level")

    class Meta:
        model = IastAssetVulV2
        exclude = ["vul_name_zh", "vul_detail_zh"]

    def get_vul_name(self, obj: IastAssetVulV2) -> str:
        if get_sca_language_profile()["language"] == "zh":
            return obj.vul_name_zh or obj.vul_name
        return obj.vul_name

    def get_vul_detail(self, obj: IastAssetVulV2) -> str:
        if get_sca_language_profile()["language"] == "zh":
            return obj.vul_detail_zh or obj.vul_detail
        return obj.vul_detail
