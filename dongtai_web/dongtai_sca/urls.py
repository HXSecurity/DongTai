from django.urls import include, path

from dongtai_web.dongtai_sca.views.asset_projects import AssetProjects
from dongtai_web.dongtai_sca.views.package import PackageList, AssetAggrDetailAssetIds
from dongtai_web.dongtai_sca.views.newpackage import PackageList
from dongtai_web.dongtai_sca.views.newpackagedetail import PackageDetail
from dongtai_web.dongtai_sca.views.newpackagevuldetail import PackageVulDetail
from dongtai_web.dongtai_sca.views.newpackagesummary import NewPackageSummary
from dongtai_web.dongtai_sca.views.newpackagevuls import NewPackageVuls
from dongtai_web.dongtai_sca.views.newpackageprojects import NewPackageRelationProject
from dongtai_web.dongtai_sca.views.newpackageprojectversions import NewPackageRelationProjectVersion
from dongtai_web.dongtai_sca.views.package_vul import OnePackageVulList, AssetPackageVulList, AssetPackageVulDetail
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('package/', PackageList.as_view()),
    path('package_vul/', OnePackageVulList.as_view()),
    path('asset_projects/<int:aggr_id>', AssetProjects.as_view()),
    path('asset_vuls/<int:aggr_id>', AssetPackageVulList.as_view()),
    path('asset_vul_detail/<int:vul_id>', AssetPackageVulDetail.as_view()),
    path('asset_ids/<int:aggr_id>', AssetAggrDetailAssetIds.as_view()),
]

v2_urlpatterns = [
    path('package/', PackageList.as_view()),
    path('package/<str:package_name>/<str:package_version>/detail',
         PackageDetail.as_view()),
    path('package_summary/', NewPackageSummary.as_view()),
    path('package_vuls/<str:package_name>/<str:package_version>',
         NewPackageVuls.as_view()),
    path('package_vul/<str:vul_id>', PackageVulDetail.as_view()),
    path('package/<str:package_name>/<str:package_version>/relation_projects',
         NewPackageRelationProject.as_view()),
    path(
        'package/<str:package_name>/<str:package_version>/relation_project/<int:project_id>',
        NewPackageRelationProjectVersion.as_view()),
]

urlpatterns = [
    path('sca/v1/', include(urlpatterns), name='ScaAPI'),
    path('sca/v2/', include(v2_urlpatterns), name='ScaAPI'),
]
