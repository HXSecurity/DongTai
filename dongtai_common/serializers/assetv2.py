from rest_framework import serializers

from dongtai_common.models.assetv2 import (
    AssetV2Global,
)
from dongtai_web.dongtai_sca.scan.utils import get_language


class PackeageScaAssetDetailSerializer(serializers.ModelSerializer):
    affected_versions = serializers.ListField(
        source="package_fullname.affected_versions"
    )
    unaffected_versions = serializers.ListField(
        source="package_fullname.unaffected_versions"
    )
    language = serializers.SerializerMethodField()
    level_name = serializers.CharField(source="get_level_display")
    level_id = serializers.IntegerField(source="level")
    vul_count_groupby_level = serializers.ListField(
        source="get_vul_count_groupby_level"
    )

    class Meta:
        model = AssetV2Global
        fields = [
            "id",
            "package_name",
            "signature_algorithm",
            "signature_value",
            "version",
            "level_id",
            "level",
            "level_name",
            "vul_count",
            "vul_critical_count",
            "vul_high_count",
            "vul_medium_count",
            "vul_low_count",
            "vul_info_count",
            "license_list",
            "language_id",
            "affected_versions",
            "unaffected_versions",
            "aql",
            "language",
            "vul_count_groupby_level",
        ]

    def get_language(self, obj) -> str:
        return get_language(obj.language_id)
