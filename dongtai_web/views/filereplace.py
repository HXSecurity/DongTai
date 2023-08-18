######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : filereplace
# @created     : Friday Oct 08, 2021 11:42:57 CST
#
# @description :
######################################################################


import logging
import os

from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema

from dongtai_common.endpoint import R, TalentAdminEndPoint
from dongtai_conf.settings import MEDIA_ROOT

logger = logging.getLogger("dongtai-webapi")

FILES_ALLOWED_MODIFIY = ("logo.png", "logo_en.png", "favicon.ico")
FILES_PATH = "assets/img/"
FILES_PATH_BACKUP = "backup"
FILES_SIZE_LIMIT = {
    "logo.png": 1024 * 1024 * 2,
    "favicon.ico": 1024 * 128,
    "logo_en.png": 1024 * 1024 * 2,
}
FILES_FORMAT = {
    "logo.png": ".png",
    "favicon.ico": ".ico",
    "logo_en.png": ".png",
}

FILES_CONTENT_TYPE = {
    "logo.png": ["image/png"],
    "favicon.ico": [
        "image/vnd.microsoft.icon",
        "image/x-icon",
        "image/ico",
        "image/icon",
        "text/ico",
        "application/ico",
    ],
    "logo_en.png": ["image/png"],
}


class FileReplace(TalentAdminEndPoint):
    @extend_schema(summary="替换文件", tags=[_("Profile")])
    def post(self, request, filename: str):
        if filename not in FILES_ALLOWED_MODIFIY:
            return R.failure(msg=_("this file is disallowed to modifyupload failed,this file is disallowed to modify."))
        try:
            file_size = FILES_SIZE_LIMIT[filename]
            file_format = FILES_FORMAT[filename]
            file_content_type = FILES_CONTENT_TYPE[filename]
            uploadfile = request.data["file"]
            if (
                uploadfile.name.endswith(file_format)
                and uploadfile.size <= file_size
                and uploadfile.content_type in file_content_type
            ):
                pass
            else:
                return R.failure(msg=_("upload error"))
            filepath = os.path.join(MEDIA_ROOT, FILES_PATH, filename)
            with open(filepath, "wb+") as fp:
                for chunk in uploadfile.chunks():
                    fp.write(chunk)
            return R.success(msg=_("upload sussess"))
        except Exception as e:
            logger.exception("uncatched exception: ", exc_info=e)
            with open(filepath, "wb+") as fp:
                backup_filepath = os.path.join(MEDIA_ROOT, FILES_PATH, FILES_PATH_BACKUP, filename)
                with open(backup_filepath, "rb+") as backup_fp:
                    write_obj = backup_fp.read()
                fp.write(write_obj)
            return R.failure(msg=_("upload error, fail back to default"))
