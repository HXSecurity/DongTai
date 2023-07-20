######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : test_agent_hardencode_vuln
# @created     : 星期六 12月 18, 2021 11:40:31 CST
#
# @description :
######################################################################


#
#
# class AgentHardencodeTestCase(AgentTestCase):
#
#    def test_agent_hardencode_vuln(self):
#            },
#
#        strategy = IastStrategyModel.objects.filter(user_id=1,
#                                                    vul_type='硬编码').first()
#        if strategy and strategy.state == 'enable':
#            assert IastVulnerabilityModel.objects.filter(
#                strategy=strategy).exists()
#
#    def test_agent_hardencode_vuln_other(self):
#            },
#        strategy = IastStrategyModel.objects.filter(user_id=1,
#                                                    vul_type='硬编码').first()
#        if strategy and strategy.state == 'enable':
#            assert IastVulnerabilityModel.objects.filter(
#                full_stack=json.dumps(jsondata['detail'])).exists()
#                full_stack=json.dumps(jsondata['detail'])).first()
#            assert vul is not None
#            if vul:
#                assert vul.top_stack == "字段:{}".format(
#                    jsondata['detail']['field'])
#                assert vul.bottom_stack == "硬编码值:{}".format(
#                    jsondata['detail']['value'])
