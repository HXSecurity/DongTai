######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : hardencode_vul_handler
# @created     : 星期五 12月 17, 2021 19:52:55 CST
#
# @description :
######################################################################


import json
import logging
import random
import time

from dongtai_common.models.hook_type import HookType
from dongtai_common.models.strategy import IastStrategyModel
from dongtai_common.models.vulnerablity import IastVulnerabilityModel
from dongtai_common.models.project import IastProject
from dongtai_common.utils import const
from dongtai_conf import settings
from dongtai_protocol.report.handler.report_handler_interface import IReportHandler
from dongtai_protocol.report.report_handler_factory import ReportHandler
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import ValidationError
from dongtai_web.vul_log.vul_log import log_vul_found
from dongtai_common.models.agent import IastAgent


from _typeshed import Incomplete
logger: Incomplete = logging.getLogger('dongtai.openapi')

class HardEncodeVulSerializer(serializers.Serializer):
    class_: Incomplete = serializers.CharField(default=None,
                                   required=False,
                                   help_text=_("class name"))
    field: Incomplete = serializers.CharField(default=None,
                                  required=False,
                                  help_text=_("field"))

    value: Incomplete = serializers.CharField(default=None, required=False)
    is_jdk: Incomplete = serializers.BooleanField(default=None, required=False)

    file_: Incomplete = serializers.CharField(default=None, required=False)



@ReportHandler.register(const.REPORT_VULN_HARDCODE)
class HardEncodeVulHandler(IReportHandler):
    validated: bool
    def parse(self) -> None:
        ser = HardEncodeVulSerializer(data=self.detail)
        try:
            if ser.is_valid(True):
                pass
        except ValidationError as e:
            self.validated = False
            return
        self.validated = True
        for k, v in ser.validated_data.items():
            setattr(self, k, v)

    def save(self) -> None:
        strategy = IastStrategyModel.objects.filter(user_id=1,
                                                    vul_type='硬编码').first()
        if not strategy or strategy.state != 'enable':
            return
        project_agents = IastAgent.objects.filter(
            project_version_id=self.agent.project_version_id)
        iast_vul = IastVulnerabilityModel.objects.filter(
            strategy_id=strategy.id,
            uri=self.detail.get('class', ''),
            http_method='',
            agent__in=project_agents).order_by('-latest_time').first()
        timestamp = int(time.time())
        if iast_vul:
            iast_vul.uri = self.detail.get('file', ''),
            iast_vul.url = self.detail.get('class', ''),
            iast_vul.latest_time = timestamp,
            iast_vul.taint_position = self.field,
            iast_vul.taint_value = self.value,
            iast_vul.level_id = strategy.level_id,
            iast_vul.full_stack = json.dumps(self.detail),
            iast_vul.top_stack = "字段:{}".format(self.field),
            iast_vul.bottom_stack = "硬编码值:{}".format(self.value),
            iast_vul.save()
        else:
            iast_vul = IastVulnerabilityModel.objects.create(
                hook_type_id=-1,
                strategy_id=strategy.id,
                uri=self.detail.get('class', ''),
                url=self.detail.get('file', ''),
                http_method='',
                http_scheme='',
                http_protocol='',
                req_header='',
                req_params='',
                req_data='',
                res_header='',
                res_body='',
                context_path='',
                counts=1,
                taint_position=self.field,
                status_id=settings.CONFIRMED,
                first_time=timestamp,
                latest_time=timestamp,
                client_ip='',
                taint_value=self.value,
                level_id=strategy.level_id,
                full_stack=json.dumps(self.detail),
                top_stack="字段:{}".format(self.field),
                method_pool_id=-1,
                bottom_stack="硬编码值:{}".format(self.value),
                agent=self.agent)
        IastVulnerabilityModel.objects.filter(
            strategy_id=strategy.id,
            uri=self.detail.get('file', ''),
            http_method='',
            agent__in=project_agents,
            pk__lt=iast_vul.id).delete()
        log_vul_found(iast_vul.agent.user_id, iast_vul.agent.bind_project.name,
                      iast_vul.agent.bind_project_id, iast_vul.id,
                      iast_vul.strategy.vul_name)
