from dongtai_common.models import User
from dongtai_common.models.asset import Asset
from dongtai_common.models.asset_aggr import AssetAggr
from dongtai_common.models.asset_vul import IastAssetVul, IastAssetVulTypeRelation, IastVulAssetRelation
from dongtai_web.dongtai_sca.models import Package, VulPackageVersion, VulPackage, VulPackageRange, Vul, VulCveRelation, \
    PackageLicenseInfo, \
    PackageLicenseLevel
from django.http import JsonResponse
from rest_framework import views
from django.forms.models import model_to_dict
from dongtai_common.endpoint import R, AnonymousAndUserEndPoint, UserEndPoint
from django.utils.translation import gettext_lazy as _
from dongtai_web.dongtai_sca.common.sca_vul import GetScaVulData

LEVEL_MAP = {'critical': '严重', 'high': '高危', 'medium': '中危', 'low': '低危'}


class OnePackageVulList(AnonymousAndUserEndPoint):
    # 查找单个漏洞下，所有的修复的高版本
    def find_fixed_versions(self, vul_package_id, ecosystem, name, version):
        vul_package_ranges = VulPackageRange.objects.filter(
            vul_package_id=vul_package_id,
            ecosystem=ecosystem, name=name,
            type__in=['ECOSYSTEM', 'SEMVER'],
            # introduced__lte=version,
            fixed_vcode__gte=version
        ).all()
        fixed_versions = []
        for vul_package_range in vul_package_ranges:
            fixed_versions.append(vul_package_range.fixed)
        return fixed_versions

    def get(self, request):
        filter_fields = ['hash', 'aql', 'ecosystem', 'name', 'version']
        _filter = Package.objects.filter()
        kwargs = {}
        for filter_field in filter_fields:
            _val = request.GET.get(filter_field, "")
            if _val != "":
                kwargs[filter_field] = request.GET.get(filter_field, "")

        ecosystem = request.GET.get('ecosystem', '')
        name = request.GET.get('name', '')
        version = request.GET.get('version', '')

        package = _filter.filter(**kwargs).first()
        print(package)
        if package is not None:
            ecosystem = package.ecosystem
            name = package.name
            version = package.version

        version_code = ""
        version_list = version.split('.')[0:4]
        while len(version_list) != 5:
            version_list.append("0")
        for _version in version_list:
            version_code += _version.zfill(5)

        vul_list = []
        vul_package_ids = []
        vul_package_ranges = VulPackageRange.objects.filter(
            ecosystem=ecosystem, name=name,
            introduced_vcode__lte=version_code, fixed_vcode__gt=version_code
        ).all()[0:1000]

        for vul_package_range in vul_package_ranges:
            vul_package_ids.append(vul_package_range.vul_package_id)

        vul_package_versions = VulPackageVersion.objects.filter(
            ecosystem=ecosystem, name=name, version=version
        ).all()[0:1000]
        for vul_package_version in vul_package_versions:
            vul_package_ids.append(vul_package_version.vul_package_id)

        for vul_package_id in vul_package_ids:
            vul_package = VulPackage.objects.get(pk=vul_package_id)
            vul = Vul.objects.get(pk=vul_package.vul_id)
            vul_list.append(
                {
                    "vul": model_to_dict(vul),
                    "vul_package": model_to_dict(vul_package),
                    "fixed_versions": self.find_fixed_versions(
                        vul_package_id,
                        ecosystem,
                        name,
                        version_code
                    )
                }
            )
        if package is not None:
            package = model_to_dict(package)

        result = {
            'data': {
                "vul_list": vul_list,
                "package": package,
            },
            'msg': 'success',
            'status': 201
        }
        return JsonResponse(result)


class AssetPackageVulList(UserEndPoint):
    name = "api-v1-sca-package-vuls"
    description = ""

    def get(self, request, aggr_id):
        auth_users = self.get_auth_users(request.user)
        asset_queryset = self.get_auth_assets(auth_users)
        asset_aggr = AssetAggr.objects.filter(id=aggr_id).first()
        if not asset_aggr:
            return R.failure(msg=_('Components do not exist or no permission to access'))

        asset_queryset_exist = asset_queryset.filter(signature_value=asset_aggr.signature_value,
                                                     version=asset_aggr.version, dependency_level__gt=0).exists()
        if not asset_queryset_exist:
            return R.failure(msg=_('Components do not exist or no permission to access'))

        vul_list = []
        auth_asset_vuls = self.get_auth_asset_vuls(asset_queryset)
        asset_vuls = IastAssetVul.objects.filter(aql=asset_aggr.package_name,
                                                 package_hash=asset_aggr.signature_value,
                                                 package_version=asset_aggr.version).all()
        for a_vul in asset_vuls:
            if a_vul.id in auth_asset_vuls:
                vul_type_relation = IastAssetVulTypeRelation.objects.filter(asset_vul_id=a_vul.id)
                vul_type_str = ""
                if vul_type_relation:
                    vul_types = [_i.asset_vul_type.name for _i in vul_type_relation]
                    vul_type_str = ','.join(vul_types)

                vul_list.append({
                    "asset_vul_id": a_vul.id,
                    "vul_title": a_vul.vul_name,
                    "cve_id": a_vul.cve_code,
                    "vul_type": vul_type_str,
                    "level_id": a_vul.level.id,
                    "level": a_vul.level.name_value,
                })

        return R.success(data=vul_list)


class AssetPackageVulDetail(UserEndPoint):
    name = "api-v1-sca-package-vul-detail"
    description = ""

    def get(self, request, vul_id):
        # 组件漏洞基础 数据读取
        asset_vul = IastAssetVul.objects.filter(id=vul_id).first()
        # 用户鉴权
        auth_users = self.get_auth_users(request.user)
        asset_queryset = self.get_auth_assets(auth_users)
        auth_asset_vuls = self.get_auth_asset_vuls(asset_queryset)

        # 判断是否有权限
        if not asset_vul or vul_id not in auth_asset_vuls:
            return R.failure(msg=_('Vul do not exist or no permission to access'))

        data = GetScaVulData(asset_vul, asset_queryset)

        return R.success(data=data)
