######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : filereplace
# @created     : Friday Oct 08, 2021 11:42:57 CST
#
# @description :
######################################################################




from dongtai.endpoint import R, TalentAdminEndPoint
import logging
from django.utils.translation import gettext_lazy as _
import os
from webapi.settings import MEDIA_ROOT
from rest_framework.parsers import FileUploadParser
logger = logging.getLogger('dongtai-webapi')

FILES_ALLOWED_MODIFIY = ("logo.png", "logo_en.png", "favicon.ico")
FILES_PATH = 'assets/img/'
FILES_PATH_BACKUP = 'backup'

class FileReplace(TalentAdminEndPoint):
    def post(self, request, filename: str):
        if filename not in FILES_ALLOWED_MODIFIY:
            return R.failure(msg=_(
                "this file is disallowed to modifyupload failed,this file is disallowed to modify."
            ))
        try:
            filepath = os.path.join(MEDIA_ROOT, FILES_PATH, filename)
            with open(filepath, 'wb+') as fp:
                for chunk in request.data['file'].chunks():
                    fp.write(chunk)
            return R.success(msg=_("upload sussess"))
        except Exception as e:
            logger.error(e)
            with open(filepath, 'wb+') as fp:
                backup_filepath = os.path.join(MEDIA_ROOT, FILES_PATH,
                                               FILES_PATH_BACKUP, filename)
                with open(backup_filepath, 'rb+') as backup_fp:
                    write_obj = backup_fp.read()
                fp.write(write_obj)
            return R.failure(msg=_("upload error, fail back to default"))
