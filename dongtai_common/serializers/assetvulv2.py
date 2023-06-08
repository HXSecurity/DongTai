
from rest_framework import serializers
from dongtai_common.models.asset_vul_v2 import IastAssetVulV2

class PackeageVulSerializer(serializers.ModelSerializer):

    class Meta:
        model = IastAssetVulV2
        fields = '__all__'

