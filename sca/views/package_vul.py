from sca.models import Package, VulPackageVersion, VulPackage, VulPackageRange, Vul
from django.http import JsonResponse
from rest_framework import views
from django.forms.models import model_to_dict
from dongtai.endpoint import R, AnonymousAndUserEndPoint

class OnePackageVulList(AnonymousAndUserEndPoint):

    # 查找单个漏洞下，所有的修复的高版本
    def find_fixed_versions(self, vul_package_id, ecosystem, name, version):
        vul_package_ranges = VulPackageRange.objects.filter(
            vul_package_id=vul_package_id,
            ecosystem=ecosystem, name=name,
            type__in=['ECOSYSTEM', 'SEMVER'],
            # introduced__lte=version,
            fixed__gte=version
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

        vul_list = []
        vul_package_ids = []
        vul_package_ranges = VulPackageRange.objects.filter(
            ecosystem=ecosystem, name=name, type="SEMVER",
            introduced__gte=version, fixed__lte=version
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
                        version
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
