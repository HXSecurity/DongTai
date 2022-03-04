######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : hardencode_vul_handler
# @created     : 星期五 12月 17, 2021 19:52:55 CST
#
# @description :
######################################################################


import json
import logging
import time

from dongtai.models.hook_type import HookType
from dongtai.models.strategy import IastStrategyModel
from dongtai.models.vulnerablity import IastVulnerabilityModel
from dongtai.models.project import IastProject
from dongtai.utils import const

from AgentServer import settings
from apiserver.report.handler.report_handler_interface import IReportHandler
from apiserver.report.report_handler_factory import ReportHandler
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import ValidationError


logger = logging.getLogger('dongtai.openapi')

class HardEncodeVulSerializer(serializers.Serializer):
    class_ = serializers.CharField(default=None,
                                   required=False,
                                   help_text=_("class name"))
    field = serializers.CharField(default=None,
                                  required=False,
                                  help_text=_("field"))

    value = serializers.CharField(default=None, required=False)
    is_jdk = serializers.BooleanField(default=None, required=False)

    file_ = serializers.CharField(default=None, required=False)



@ReportHandler.register(const.REPORT_VULN_HARDCODE)
class HardEncodeVulHandler(IReportHandler):
    def parse(self):
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

    def save(self):
        strategy = IastStrategyModel.objects.filter(user_id=1,
                                                    vul_type='硬编码').first()
        if not strategy or strategy.state != 'enable':
            return
        IastVulnerabilityModel.objects.create(
            hook_type_id=-1,
            strategy_id=strategy.id,
            uri=self.detail.get('file', ''),
            url=self.detail.get('class', ''),
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
            first_time=int(time.time()),
            latest_time=int(time.time()),
            client_ip='',
            taint_value=self.value,
            level_id=strategy.level_id,
            full_stack=json.dumps(self.detail),
            top_stack="字段:{}".format(self.field),
            method_pool_id=-1,
            bottom_stack="硬编码值:{}".format(self.value),
            agent=self.agent)
