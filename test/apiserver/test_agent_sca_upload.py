######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : test_agent_sca_upload
# @created     : 星期一 12月 20, 2021 20:34:48 CST
#
# @description :
######################################################################


from test.apiserver.test_agent_base import AgentTestCase


class ScaUploadTestCase(AgentTestCase):
    def test_agent_sca_upload(self):
        data = {
            "detail": {
                "packagePath": "/Users/xxx/spring-boot/2.3.2.RELEASE/spring-boot-2.3.2.RELEASE.jar",
                "agentId": self.agent_id,
                "packageSignature": "efd5812bc736735e71447a51701becd14c2bede0",
                "packageName": "spring-boot-2.3.2.RELEASE.jar",
                "packageAlgorithm": "SHA-1",
            },
            "type": 17,
        }
        res = self.agent_report(data)
        assert res.status_code == 200

    def test_agent_sca_bulk_upload(self):
        data = {
            "detail": {
                "agentId": self.agent_id,
                "packages": [
                    {
                        "packagePath": "/Users/xxx/spring-boot/2.3.2.RELEASE/spring-boot-2.3.2.RELEASE.jar",
                        "packageSignature": "efd5812bc736735e71447a51701becd14c2bede0",
                        "packageName": "spring-boot-2.3.2.RELEASE.jar",
                        "packageAlgorithm": "SHA-1",
                    }
                ],
            },
            "type": 18,
        }
        res = self.agent_report(data)
        assert res.status_code == 200
