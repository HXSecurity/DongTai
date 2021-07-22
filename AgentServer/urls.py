"""AgentServer URL Configuration

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

from django.conf.urls import url
from django.urls import path, include
from dongtai.doc import schema_view

urlpatterns = [
    url(r'^doc/$', schema_view(
        title='DongTai OpenAPI',
        version='v1',
        description='DongTai OpenAPI服务接口文档',
        public=True if os.getenv('active.profile', 'PROD') == 'TEST' else False
    ).with_ui('swagger', cache_timeout=None), name='schema-swagger-ui'),
    path('api/v1/', include('apiserver.urls')),
]
