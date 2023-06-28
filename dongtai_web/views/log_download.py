import os
import logging
import zipfile
from dongtai_common.endpoint import UserEndPoint
from io import BytesIO
from dongtai_common.models.agent import IastAgent
from enum import Enum
from django.http import FileResponse
from rest_framework import viewsets
from result import Ok, Err, Result
from functools import partial
from wsgiref.util import FileWrapper
from django.http import HttpResponseNotFound
from dongtai_common.models.message import IastMessage
import threading
from django.db.models import Q
from django.db import transaction
from dongtai_conf.settings import TMP_COMMON_PATH
from tempfile import NamedTemporaryFile
from dongtai_common.endpoint import R

logger = logging.getLogger('dongtai-webapi')


class ResultType(Enum):
    OK = 1
    ERR = 2


def nothing_resp():
    return HttpResponseNotFound("找不到相关日志数据")


class AgentLogDownload(UserEndPoint, viewsets.ViewSet):

    def get_single(self, request, pk):
        try:
            a = int(pk) > 0
            if not a:
                return nothing_resp()
        except BaseException:
            return nothing_resp()
        department = request.user.get_relative_department()
        if IastAgent.objects.filter(pk=pk,
                                    department__in=department).exists():
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

    def batch_task_add(self, request):
        mode = request.data.get('mode', 1)
        department = request.user.get_relative_department()
        q = Q(department__in=department)
        if mode == 1:
            ids = request.data.get('ids', [])
            q = q & Q(pk__in=ids)
        elif mode == 2:
            q = q

        def generate_zip_thread():
            generate_agent_log_zip(q, request.user.id)

        t1 = threading.Thread(target=generate_zip_thread, daemon=True)
        t1.start()
        return R.success()

    def batch_log_download(self, request, pk):
        try:
            a = int(pk) > 0
            if not a:
                return nothing_resp()
            return FileResponse(open(
                os.path.join(TMP_COMMON_PATH, f'batchagent/{pk}.zip'), 'rb'),
                filename='agentlog.zip')
        except FileNotFoundError as e:
            logger.info(e)
            return nothing_resp()
        except Exception as e:
            logger.info(e)
            return nothing_resp()


def generate_path(agent_id):
    return os.path.join(TMP_COMMON_PATH, f'agent/{agent_id}/')


def get_newest_log_zip(agent_id: int) -> Result:
    path = generate_path(agent_id)
    res = file_newest_2_file_under_path(path)
    if isinstance(res, Err):
        return res
    res = getzipfilesinmemorty(res.value)
    return res


def getzipfilesinmemorty(filenames: list) -> Result[BytesIO, str]:
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


def file_newest_N_file_under_path(path: str, N: int) -> Result[list[str], str]:
    try:
        files = [
            f for f in os.listdir(path)
            if os.path.isfile(os.path.join(path, f))
        ]
        paths = [os.path.join(path, basename) for basename in files]
        return Ok(sorted(paths, key=os.path.getctime, reverse=True)[:N])
    except (FileNotFoundError, ValueError) as e:
        return Err('file path error')
    except Exception as e:
        logger.error(e, exc_info=True)
        return Err('unexcept error')


file_newest_file_under_path = partial(file_newest_N_file_under_path, N=1)
file_newest_2_file_under_path = partial(file_newest_N_file_under_path, N=2)


def zip_file_write(msg_id, items):
    from zipfile import ZipFile
    zipfilepath = os.path.join(TMP_COMMON_PATH, f'batchagent/{msg_id}.zip')
    zip_subdir = "logs"
    with ZipFile(zipfilepath, 'w') as zipObj:
        with NamedTemporaryFile() as tmpfile:
            zipObj.write(tmpfile.name)
        for i in items:
            for k in i:
                path1, filename = os.path.split(k)
                path2, agent_id = os.path.split(path1)
                zipObj.write(
                    k, os.path.join(zip_subdir, f'/{agent_id}/', filename))
    return zipfilepath


def get_zip_together(agents_ids, msg_id):
    from zipfile import ZipFile
    res = map(
        lambda x: x.value,
        filter(
            lambda x: isinstance(x, Ok),
            map(file_newest_2_file_under_path, map(generate_path,
                                                   agents_ids))))
    return zip_file_write(msg_id, res)


@transaction.atomic
def generate_agent_log_zip(q, user_id):
    agent_ids = IastAgent.objects.filter(q).values_list('id', flat=True)
    msg = IastMessage.objects.create(message='AGENT日志导出成功',
                                     message_type_id=2,
                                     relative_url='/api/v1/agent/log/tmp',
                                     to_user_id=user_id)

    zip_file_size = os.path.getsize(get_zip_together(agent_ids, msg.id))
    msg.relative_url = f'/api/v1/agent/log/batch/{msg.id}'
    if int(zip_file_size) < 500:
        msg.message = 'agent日志获取失败，请登录项目服务器获取'
        msg.relative_url = f'/api/v1/agent/log/batch/null'
    msg.save()
