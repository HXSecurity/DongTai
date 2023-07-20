#!/usr/bin/env python
# datetime:2021/1/12 下午6:59

from django.urls import include, path

from dongtai_protocol.views.agent_config import (
    AgentConfigv2View,
    AgentConfigView,
)
from dongtai_protocol.views.agent_configv2 import AgentConfigAllinOneView
from dongtai_protocol.views.agent_download import AgentDownload
from dongtai_protocol.views.agent_limit import LimitView
from dongtai_protocol.views.agent_register import AgentRegisterEndPoint
from dongtai_protocol.views.agent_update import AgentUpdateEndPoint
from dongtai_protocol.views.engine_auto_deploy import AutoDeployEndPoint
from dongtai_protocol.views.engine_download import EngineDownloadEndPoint
from dongtai_protocol.views.engine_heartbeat import EngineHeartBeatEndPoint
from dongtai_protocol.views.engine_status import EngineAction, EngineUpdateEndPoint
from dongtai_protocol.views.except_action import AgentActionV2EndPoint
from dongtai_protocol.views.health import HealthView
from dongtai_protocol.views.health_oss import OSSHealthView
from dongtai_protocol.views.hook_profiles import HookProfilesEndPoint
from dongtai_protocol.views.hook_profilesv2 import HookProfilesV2EndPoint
from dongtai_protocol.views.properties import PropertiesEndPoint
from dongtai_protocol.views.report_upload import ReportUploadEndPoint
from dongtai_protocol.views.startuptime import (
    StartupTimeEndPoint,
    StartupTimeGzipEndPoint,
)

urlpatterns = [
    path("agent/download", AgentDownload.as_view()),
    path("agent/limit", LimitView.as_view()),
    path("agent/startuptime", StartupTimeEndPoint.as_view()),
    path("agent/gzipstartuptime", StartupTimeGzipEndPoint.as_view()),
    # agent get destroy strategy
    path("agent/threshold", AgentConfigView.as_view()),
    path("agent/thresholdv2", AgentConfigv2View.as_view()),
    path("deploy/auto", AutoDeployEndPoint.as_view()),
    path("engine/heartbeat", EngineHeartBeatEndPoint.as_view()),
    path("engine/download", EngineDownloadEndPoint.as_view()),
    path("agent/register", AgentRegisterEndPoint.as_view()),
    path("agent/update", AgentUpdateEndPoint.as_view()),
    path("engine/update", EngineUpdateEndPoint.as_view()),
    path("engine/update/<int:status>", EngineUpdateEndPoint.as_view()),
    path("profiles", HookProfilesEndPoint.as_view()),
    path("profilesv2", HookProfilesV2EndPoint.as_view()),
    path("properties", PropertiesEndPoint.as_view()),
    path("report/upload", ReportUploadEndPoint.as_view()),
    path("engine/action", EngineAction.as_view()),
    # todo 增加重放请求获取接口,用于后续逻辑漏洞/漏洞验证等功能,暂时先不实现
    path("health", HealthView.as_view()),
    path("oss/health", OSSHealthView.as_view()),
    path(
        "except_action", AgentActionV2EndPoint.as_view({"get": "except_running_status"})
    ),
    path(
        "actual_action",
        AgentActionV2EndPoint.as_view({"post": "actual_running_status"}),
    ),
    path("agent/config", AgentConfigAllinOneView.as_view()),
]

urlpatterns = [
    path("api/v1/", include(urlpatterns), name="OpenAPI"),
]
