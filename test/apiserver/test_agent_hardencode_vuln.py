######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : test_agent_hardencode_vuln
# @created     : 星期六 12月 18, 2021 11:40:31 CST
#
# @description :
######################################################################


from test.apiserver.test_agent_base import AgentTestCase
from dongtai_common.models.agent import IastAgent
from dongtai_common.models.agent_method_pool import MethodPool
from dongtai_common.models.strategy import IastStrategyModel
from dongtai_common.models.vulnerablity import IastVulnerabilityModel
import json

#
#
# class AgentHardencodeTestCase(AgentTestCase):
#
#    def test_agent_hardencode_vuln(self):
#        json_ = {
#            "detail": {
#                "file": "SpringsecApplication.java",
#                "field": "PASSWORD",
#                "isJdk": False,
#                "class": "org.iast.springsec.SpringsecApplication",
#                "value": "1111"
#            },
#            "type": 37
#        }
#
#        res = self.agent_report(json_)
#        assert res.status_code == 200
#        strategy = IastStrategyModel.objects.filter(user_id=1,
#                                                    vul_type='硬编码').first()
#        if strategy and strategy.state == 'enable':
#            assert IastVulnerabilityModel.objects.filter(
#                strategy=strategy).exists()
#
#    def test_agent_hardencode_vuln_other(self):
#        jsondata = {
#            "detail": {
#                "agentId": self.agent_id,
#                "file": "DriverDataSource.java",
#                "field": "PASSWORD",
#                "isJdk": False,
#                "class": "com.zaxxer.hikari.util.DriverDataSource",
#                "value": "password"
#            },
#            "type": 37
#        }
#        res = self.agent_report(jsondata)
#        assert res.status_code == 200
#        strategy = IastStrategyModel.objects.filter(user_id=1,
#                                                    vul_type='硬编码').first()
#        if strategy and strategy.state == 'enable':
#            assert IastVulnerabilityModel.objects.filter(
#                strategy=strategy,
#                full_stack=json.dumps(jsondata['detail'])).exists()
#            vul = IastVulnerabilityModel.objects.filter(
#                strategy=strategy,
#                full_stack=json.dumps(jsondata['detail'])).first()
#            assert vul is not None
#            if vul:
#                assert vul.uri == jsondata['detail']['class']
#                assert vul.url == jsondata['detail']['file']
#                assert vul.taint_position == jsondata['detail']['field']
#                assert vul.top_stack == "字段:{}".format(
#                    jsondata['detail']['field'])
#                assert vul.bottom_stack == "硬编码值:{}".format(
#                    jsondata['detail']['value'])
