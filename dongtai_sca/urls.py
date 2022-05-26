from django.urls import include, path

from dongtai_sca.views.asset_projects import AssetProjects, AssetVulProjects, ProjectsAssets
from dongtai_sca.views.package import PackageList, AssetAggrDetailAssetIds
from dongtai_sca.views.package_vul import OnePackageVulList, AssetPackageVulList, AssetPackageVulDetail
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('package/', PackageList.as_view()),
    path('package_vul/', OnePackageVulList.as_view()),
    path('asset_projects/<int:aggr_id>', AssetProjects.as_view()),
    path('asset_vul_projects/<int:vul_id>', AssetVulProjects.as_view()),
    path('vul_project_assets', ProjectsAssets.as_view()),
    path('asset_vuls/<int:aggr_id>', AssetPackageVulList.as_view()),
    path('asset_vul_detail/<int:vul_id>', AssetPackageVulDetail.as_view()),
    path('asset_ids/<int:aggr_id>', AssetAggrDetailAssetIds.as_view()),
]

urlpatterns = [path('sca/v1/', include(urlpatterns), name='ScaAPI'), ]
