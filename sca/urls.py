from django.urls import include, path
from sca.views.package import PackageList
from sca.views.package_vul import OnePackageVulList
from rest_framework import routers
router = routers.DefaultRouter()

urlpatterns = [
    path('package/', PackageList.as_view()),
    path('package_vul/', OnePackageVulList.as_view()),
]

