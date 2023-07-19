"""dongtai_conf URL Configuration

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
import os

from django.conf.urls.static import static
from django.urls import URLPattern, URLResolver, include, path

from dongtai_conf import settings

urlpatterns: list[URLResolver | URLPattern] = [
    path("", include(f"{app}.urls")) for app in settings.CUSTOM_APPS
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns.extend([path("healthcheck", include("health_check.urls"))])
if os.getenv("METRICS", None) == "true":
    urlpatterns.extend([path("", include("django_prometheus.urls"))])

if (
    os.getenv("environment", "PROD") in ("TEST", "DOC")
    or os.getenv("DOC", None) == "TRUE"
):
    from drf_spectacular.views import (
        SpectacularJSONAPIView,
        SpectacularRedocView,
        SpectacularSwaggerView,
    )

    urlpatterns.extend(
        [
            path(
                "api/XZPcGFKoxYXScwGjQtJx8u/schema/",
                SpectacularJSONAPIView.as_view(),
                name="schema",
            ),
            path(
                "api/XZPcGFKoxYXScwGjQtJx8u/schema/swagger-ui/",
                SpectacularSwaggerView.as_view(url_name="schema"),
                name="swagger-ui",
            ),
            path(
                "api/XZPcGFKoxYXScwGjQtJx8u/schema/redoc/",
                SpectacularRedocView.as_view(url_name="schema"),
                name="redoc",
            ),
        ]
    )


if os.getenv("DJANGOSILK", None) == "TRUE":
    silk_path = os.getenv(
        "DJANGOSILKPATH",
        "9671ccbd0c655fda78354dda754c9c4fb7111b7c18751b25ea8930ab87c84f94",
    )
    urlpatterns += [
        path(f"api/silk/{silk_path}/silk/", include("silk.urls", namespace="silk"))
    ]
