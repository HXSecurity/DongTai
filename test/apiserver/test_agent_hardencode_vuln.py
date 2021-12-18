######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : test_agent_hardencode_vuln
# @created     : 星期六 12月 18, 2021 11:40:31 CST
#
# @description :
######################################################################



from test.apiserver.test_agent_base import AgentTestCase
from dongtai.models.agent import IastAgent
from dongtai.models.agent_method_pool import MethodPool
from dongtai.models.strategy import IastStrategyModel
from dongtai.models.vulnerablity import IastVulnerabilityModel


class AgentHardencodeTestCase(AgentTestCase):


    def test_agent_hardencode_vuln(self):
        json = {
            "detail": {
                "file": "SpringsecApplication.java",
                "field": "PASSWORD",
                "isJdk": False,
                "class": "org.iast.springsec.SpringsecApplication",
                "value": "1111"
            },
            "type": 37
        }

        res = self.agent_report(json)
        assert res.status_code == 200
        strategy = IastStrategyModel.objects.filter(user_id=1,
                                                    vul_type='硬编码').first()
        if strategy and strategy.state == 'enable':
            assert IastVulnerabilityModel.objects.filter(
                strategy=strategy).exists()
