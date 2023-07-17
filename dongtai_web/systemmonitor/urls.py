from django.urls import include, path

from rest_framework import routers
from dongtai_web.systemmonitor.project_warning import ProjectWarningEndpoint

router = routers.DefaultRouter()

base_urlpatterns = [
    path("project_warning", ProjectWarningEndpoint.as_view()),
]

urlpatterns = [
    path("api/v1/systemmonitor/", include(base_urlpatterns)),
]
