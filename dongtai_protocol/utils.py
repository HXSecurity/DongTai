#!/usr/bin/env python
# datetime: 2021/6/1 上午9:53

# -*- coding: utf-8 -*-
import base64
import logging

import oss2
from oss2.exceptions import NoSuchKey, RequestError

from dongtai_conf import settings

logger = logging.getLogger("dongtai.openapi")


class OssDownloader:
    BUCKET_URL = "https://oss-cn-beijing.aliyuncs.com"
    BUCKET_NAME = "dongtai"

    @staticmethod
    def download_file_to_path(
        bucket_url,
        bucket_name,
        object_name,
        local_file,
        access_key="",
        access_key_secret="",
        anonymous=True,
    ):
        """

        :param access_key:
        :param access_key_secret:
        :param bucket_url:
        :param bucket_name:
        :param object_name:
        :param local_file:
        :return:
        """
        try:
            if anonymous:
                auth = oss2.AnonymousAuth()
            else:
                auth = oss2.Auth(access_key, access_key_secret)
            bucket = oss2.Bucket(auth, bucket_url, bucket_name)
            bucket.get_object_to_file(object_name, local_file)
        except NoSuchKey:
            # NoSuchKey表示oss云端文件不存在,通知管理员
            logger.exception(
                f"oss download failure, reason: remote file not found, filename: {object_name}"
            )
            return False
        except Exception as e:
            logger.exception("oss download failure, reason: ", exc_info=e)
            return False
        else:
            return True

    @staticmethod
    def download_file(object_name, local_file):
        return OssDownloader.download_file_to_path(  # access_key=settings.ACCESS_KEY,
            bucket_url=OssDownloader.BUCKET_URL,
            bucket_name=OssDownloader.BUCKET_NAME,
            object_name=object_name,
            local_file=local_file,
        )


def base64_decode(raw: str) -> str:
    try:
        return base64.b64decode(raw).decode("utf-8").strip()
    except Exception as decode_error:
        logger.exception(
            f"base64 decode error, raw: {raw}\nreason: ", exc_info=decode_error
        )
        return ""


def build_request_header(req_method, raw_req_header, uri, query_params, http_protocol):
    decode_req_header = base64_decode(raw_req_header)
    return f"{req_method} {uri + ('?' + query_params if query_params else '')} {http_protocol}\n{decode_req_header}"


STATUSMAP = {True: 1, False: 0}


def updateossstatus():
    from dongtai_protocol.views.agent_download import (
        JavaAgentDownload,
        PythonAgentDownload,
    )
    from dongtai_protocol.views.engine_download import (
        PACKAGE_NAME_LIST,
        EngineDownloadEndPoint,
    )

    try:
        status_, _ = checkossstatus()
        if not status_:
            return False, None
        import shutil

        shutil.rmtree("/tmp")
        OssDownloader.download_file(
            JavaAgentDownload.REMOTE_AGENT_FILE,
            local_file=JavaAgentDownload.LOCAL_AGENT_FILE,
        )
        OssDownloader.download_file(
            object_name=PythonAgentDownload.REMOTE_AGENT_FILE,
            local_file=PythonAgentDownload.LOCAL_AGENT_FILE,
        )
        for package_name in PACKAGE_NAME_LIST:
            EngineDownloadEndPoint.download_agent_jar(
                EngineDownloadEndPoint.REMOTE_AGENT_FILE.format(
                    package_name=package_name
                ),
                EngineDownloadEndPoint.LOCAL_AGENT_FILE.format(
                    package_name=package_name
                ),
            )
        downloadstatus = (
            JavaAgentDownload(user_id=1).download_agent()
            and PythonAgentDownload(user_id=1).download_agent()
        )
    except RequestError:
        return False, None
    except Exception as e:
        logger.info(f"Health check oss status:{e}")
        return False, None
    else:
        return downloadstatus, None


def checkossstatus():
    from oss2.exceptions import AccessDenied

    try:
        bucket = oss2.Bucket(
            oss2.AnonymousAuth(),
            settings.BUCKET_URL,
            settings.BUCKET_NAME,
            connect_timeout=4,
        )
        bucket.list_objects()
    except RequestError:
        return False, None
    except AccessDenied:
        return True, None
    except Exception as e:
        logger.info(f"Health check oss status:{e}")
        return False, None
    else:
        return True, None
