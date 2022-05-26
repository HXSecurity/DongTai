import time

from dongtai_common.endpoint import R
from dongtai_common.endpoint import UserEndPoint
from dongtai_common.models.project_report import ProjectReport
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from dongtai_web.utils import extend_schema_with_envcheck
from django.http import HttpResponse
from io import BytesIO, StringIO
from rest_framework.serializers import ValidationError
from dongtai_common.models.agent import IastAgent
import os
from enum import Enum
from django.http import FileResponse,JsonResponse
import logging
from result import Ok, Err, Result
import zipfile
from functools import partial
from wsgiref.util import FileWrapper
from dongtai_common.utils.user import get_auth_users__by_id
import json
from django.http import HttpResponseNotFound

logger = logging.getLogger('dongtai-webapi')


class ResultType(Enum):
    OK = 1
    ERR = 2

def nothing_resp():
    return HttpResponseNotFound("找不到相关日志数据")

class AgentLogDownload(UserEndPoint):

    def get(self, request, pk):
        try:
            a = int(pk) > 0
            if not a:
                return nothing_resp()
        except:
            return nothing_resp()
        if IastAgent.objects.filter(pk=pk,
                                    user__in=get_auth_users__by_id(
                                        request.user.id)).exists():
            result = get_newest_log_zip(pk)
            if isinstance(result, Err):
                return nothing_resp()
            file_ = result.value
            file_.seek(0)
            response = FileResponse(FileWrapper(file_))
            response['content_type'] = 'application/octet-stream'
            response['Content-Disposition'] = f"attachment; filename={pk}.zip"
            return response
        return nothing_resp()

def generate_path(agent_id):
    return f'/tmp/logstash/agent/{agent_id}/'


def get_newest_log_zip(agent_id: int) -> Result:
    path = generate_path(agent_id)
    res = file_newest_2_file_under_path(path)
    if isinstance(res, Err):
        return res
    res = getzipfilesinmemorty(res.value)
    return res


def getzipfilesinmemorty(filenames: list) -> Result[int, BytesIO]:
    try:
        zip_subdir = "logs"
        s = BytesIO()
        with zipfile.ZipFile(s, "w") as zf:
            for fpath in filenames:
                fdir, fname = os.path.split(fpath)
                zip_path = os.path.join(zip_subdir, fname)
                zf.write(fpath, zip_path)
            zf.close()
        return Ok(s)
    except Exception as e:
        logger.error(e, exc_info=True)
        return Err('unexcept eror')


def file_newest_N_file_under_path(path: str, N: int) -> Result[int, str]:
    try:
        files = [
            f for f in os.listdir(path)
            if os.path.isfile(os.path.join(path, f))
        ]
        paths = [os.path.join(path, basename) for basename in files]
        return Ok(sorted(paths, key=os.path.getctime)[:N])
    except (FileNotFoundError, ValueError) as e:
        return Err('file path error')
    except Exception as e:
        logger.error(e, exc_info=True)
        return Err('unexcept error')


file_newest_file_under_path = partial(file_newest_N_file_under_path, N=1)
file_newest_2_file_under_path = partial(file_newest_N_file_under_path, N=2)
