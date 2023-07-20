from django.urls import include, path
from rest_framework import routers

from dongtai_web.dongtai_sca.views.newpackage import PackageList
from dongtai_web.dongtai_sca.views.newpackagedetail import PackageDetail
from dongtai_web.dongtai_sca.views.newpackageprojects import NewPackageRelationProject
from dongtai_web.dongtai_sca.views.newpackageprojectversions import (
    NewPackageRelationProjectVersion,
)
from dongtai_web.dongtai_sca.views.newpackagesummary import NewPackageSummary
from dongtai_web.dongtai_sca.views.newpackagevuldetail import PackageVulDetail
from dongtai_web.dongtai_sca.views.newpackagevullevel import PackageVulLevels
from dongtai_web.dongtai_sca.views.newpackagevuls import NewPackageVuls

router = routers.DefaultRouter()

v2_urlpatterns = [
    path("package/", PackageList.as_view()),
    path(
        "package/<int:language_id>/<str:package_name>/<str:package_version>/detail",
        PackageDetail.as_view(),
    ),
    path("package_summary/", NewPackageSummary.as_view()),
    path(
        "package_vuls/<int:language_id>/<str:package_name>/<str:package_version>",
        NewPackageVuls.as_view(),
    ),
    path("package_vul/<str:vul_id>", PackageVulDetail.as_view()),
    path("package_vul_level", PackageVulLevels.as_view()),
    path(
        "package/<int:language_id>/<str:package_name>/<str:package_version>/relation_projects",
        NewPackageRelationProject.as_view(),
    ),
    path(
        "package/<int:language_id>/<str:package_name>/<str:package_version>/relation_project/<int:project_id>",
        NewPackageRelationProjectVersion.as_view(),
    ),
]

urlpatterns = [
    path("api/sca/v2/", include(v2_urlpatterns), name="ScaAPI"),
]
