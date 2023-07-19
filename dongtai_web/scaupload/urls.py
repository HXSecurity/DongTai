"""webapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path

from dongtai_web.scaupload.views import (
    SCADBMavenBulkDeleteView,
    SCADBMavenBulkViewSet,
    SCADBMavenViewSet,
    SCALicenseViewSet,
    SCATemplateViewSet,
)

urlpatterns = [
    path(
        "maven/bulk",
        SCADBMavenBulkViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
    ),
    path("maven/bulk/delete", SCADBMavenBulkDeleteView.as_view()),
    path(
        "maven/<int:pk>",
        SCADBMavenViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destory"}
        ),
    ),
    path("maven", SCADBMavenViewSet.as_view({"post": "create"})),
    path("license_list", SCALicenseViewSet.as_view()),
    path("maven/template/maven_sca", SCATemplateViewSet.as_view()),
]


urlpatterns = [path("api/v1/scadb/", include(urlpatterns))]
