######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : test_agent_startuptime
# @created     : 星期一 12月 20, 2021 18:48:30 CST
#
# @description :
######################################################################


from test.apiserver.test_agent_base import AgentTestCase, gzipdata


class AgentStartUptimeTestCase(AgentTestCase):
    def test_start_up_time_compalince(self):
        data = {"agentId": self.agent_id, "startupTime": 448}
        gzip_data = gzipdata(data)
        response_no_gzip = self.client.post(
            "http://testserver/api/v1/agent/startuptime",
            data=data,
        )
        response_gzip = self.client.post(
            "http://testserver/api/v1/agent/gzipstartuptime",
            data=gzip_data,
            HTTP_CONTENT_ENCODING="gzip",
            content_type="application/json",
        )
        assert response_no_gzip.status_code == 200
        assert response_gzip.status_code == 200
