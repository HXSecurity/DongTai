from test.apiserver.test_agent_base import AgentTestCase

from dongtai_common.models.api_route import IastApiRoute

data = {
    "type": 97,
    "detail": {
        "agentId": 8,
        "apiData": [
            {
                "controller": "app.iast.api.springmvc.controller.GreetingController",
                "file": "",
                "method": ["GET", "POST"],
                "description": "",
                "uri": "/request-mapping/path/{value1}/{value2}",
                "class": "app.iast.api.springmvc.controller.GreetingController",
                "parameters": [
                    {
                        "annotation": "restful访问参数",
                        "name": "value1",
                        "type": "java.lang.String",
                    },
                    {
                        "annotation": "restful访问参数",
                        "name": "value2",
                        "type": "java.lang.String",
                    },
                    {
                        "annotation": "",
                        "name": "model",
                        "type": "org.springframework.ui.Model",
                    },
                ],
                "returnType": "java.lang.String",
            }
        ],
    },
}


class ApiRouteParameterCheckTestCase(AgentTestCase):
    def test_agent_api_upload(self):
        data["detail"]["agentId"] = self.agent_id
        self.agent_report(data, agentId=self.agent_id)
        api_routes = list(IastApiRoute.objects.filter(path="/request-mapping/path/{value1}/{value2}").all())
        self.assertEqual(len(api_routes), 2)
        for route in api_routes:
            self.assertEqual(route.iastapiparameter_set.count(), 3)
            self.assertEqual(route.iastapiresponse_set.count(), 1)
