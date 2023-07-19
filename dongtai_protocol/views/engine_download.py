#!/usr/bin/env python
# datetime:2020/5/21 15:56

import logging
import os

from django.http import FileResponse
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.request import Request

from dongtai_common.endpoint import OpenApiEndPoint, R
from dongtai_conf.settings import BUCKET_NAME_BASE_URL, VERSION
from dongtai_protocol.api_schema import DongTaiParameter
from dongtai_protocol.utils import OssDownloader

logger = logging.getLogger("dongtai.openapi")

PACKAGE_NAME_LIST = (
    "dongtai-core",
    "dongtai-spy",
    "dongtai-api",
    "dongtai-grpc",
    "dongtai-log",
    "dongtai-spring-api",
    "dongtai-core-jdk6",
    "dongtai-api-jdk6",
    "dongtai-spy-jdk6",
)


class EngineDownloadEndPoint(OpenApiEndPoint):
    name = "download_core_jar_package"
    description = "iast agent-下载IAST依赖的core、inject jar包"
    LOCAL_AGENT_PATH = "/tmp/iast_cache/package"
    LOCAL_AGENT_FILE = "/tmp/iast_cache/package/{package_name}.jar"
    REMOTE_AGENT_FILE = BUCKET_NAME_BASE_URL + "java/" + VERSION + "/{package_name}.jar"

    @extend_schema(
        description="Agent Engine Download",
        parameters=[
            DongTaiParameter.ENGINE_NAME,
        ],
        responses=R,
        methods=["GET"],
        summary="下载 Agent Engine",
        tags=["Agent服务端交互协议"],
    )
    def get(self, request: Request):
        package_name = request.query_params.get("engineName")
        if package_name not in PACKAGE_NAME_LIST:
            return R.failure({"status": -1, "msg": "bad gay."})
        local_file_name = EngineDownloadEndPoint.LOCAL_AGENT_FILE.format(
            package_name=package_name
        )
        remote_file_name = EngineDownloadEndPoint.REMOTE_AGENT_FILE.format(
            package_name=package_name
        )
        logger.debug(f"download file from oss or local cache, file: {local_file_name}")
        if self.download_agent_jar(
            remote_agent_file=remote_file_name, local_agent_file=local_file_name
        ):
            try:
                response = FileResponse(open(local_file_name, "rb"))
                response["content_type"] = "application/octet-stream"
                response[
                    "Content-Disposition"
                ] = f"attachment; filename={package_name}.jar"
                return response
            except Exception as e:
                logger.error(e, exc_info=True)
                return R.failure(
                    msg="file not exit.", status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return R.failure(
                msg="file not exit.", status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @staticmethod
    def download_agent_jar(remote_agent_file, local_agent_file):
        if not os.path.exists(EngineDownloadEndPoint.LOCAL_AGENT_PATH):
            os.makedirs(EngineDownloadEndPoint.LOCAL_AGENT_PATH)
        if os.path.exists(local_agent_file):
            return True
        return OssDownloader.download_file(
            object_name=remote_agent_file, local_file=local_agent_file
        )
