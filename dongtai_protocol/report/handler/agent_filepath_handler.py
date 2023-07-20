import logging

from django.db import transaction
from django.utils.translation import gettext_lazy as _
from simhash import Simhash

from dongtai_common.models.agent import IastAgent
from dongtai_common.models.agent_thirdservice import IastThirdPartyService
from dongtai_common.models.api_route import (
    HttpMethod,
    IastApiMethod,
    IastApiMethodHttpMethodRelation,
    IastApiParameter,
    IastApiResponse,
    IastApiRoute,
)
from dongtai_common.models.project import IastProject
from dongtai_common.utils import const
from dongtai_protocol.report.handler.report_handler_interface import IReportHandler
from dongtai_protocol.report.report_handler_factory import ReportHandler

logger = logging.getLogger("dongtai.openapi")


@ReportHandler.register(const.REPORT_FILE_PATH)
class FilePathHandler(IReportHandler):
    def parse(self):
        self.filepath = self.detail.get("serviceDir")
        self.servicetype = self.detail.get("serviceType")

    def save(self):
        try:
            simhash = _data_dump(self.filepath)
            IastAgent.objects.filter(pk=self.agent_id).update(
                filepathsimhash=simhash, servicetype=self.servicetype
            )
            logger.info(
                _("filepath simhash log successed : {} servicetype: {}").format(
                    simhash, self.servicetype
                )
            )
        except Exception as e:
            logger.info(_("filepath simhash log failed, why: {}").format(e))


def _data_dump(filepath: str) -> str:
    return str(Simhash(filepath).value)
