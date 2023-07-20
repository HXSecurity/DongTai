import json
import unittest
from test import DongTaiTestCase
from test.apiserver.test_agent_base import METHODPOOL_JSON, REGISTER_JSON, gzipdata

from rest_framework.test import APITestCase

from dongtai_common.models.user import User


class MyTestCase(DongTaiTestCase):
    def test_something(self):
        self.assertEqual(True, False)

    def test_vul_recheck(self):
        from dongtai_engine.tasks import vul_recheck

        vul_recheck()

    def test_search_vul_from_replay_method_pool(self):
        from dongtai_engine.tasks import search_vul_from_replay_method_pool

        method_id = 110
        search_vul_from_replay_method_pool(method_id)

    def test_search_vul_from_method_pool(self):
        method_pool_id = 657160

        from dongtai_engine.tasks import search_vul_from_method_pool

        search_vul_from_method_pool(method_pool_id)

    def test_update_agent_status(self):
        from dongtai_engine.tasks import update_agent_status

        update_agent_status()

    def test_verify_agent_status(self):
        import time

        from dongtai_common.models.agent import IastAgent
        from dongtai_engine.tasks import is_alive

        timestamp = int(time.time())
        stopped_agents = IastAgent.objects.values("id").filter(is_running=0)
        is_running_agents = []
        for agent in stopped_agents:
            agent_id = agent["id"]
            if is_alive(agent_id=agent_id, timestamp=timestamp):
                is_running_agents.append(agent_id)
            else:
                continue
        if is_running_agents:
            IastAgent.objects.filter(id__in=is_running_agents).update(
                is_running=1, is_core_running=1
            )

    def test_update_sca(self):
        from dongtai_engine.tasks import update_one_sca

        update_one_sca(
            2379,
            "/Users/xxx/spring-boot/2.3.2.RELEASE/org.springframework:spring-beans.jar",
            "a4bb5ffad5564e4a0e25955e3a40b1c6158385b2",
            "org.springframework:spring-beans.jar",
            "SHA-1",
        )

    def test_http_header(self):
        from dongtai_common.models.agent import IastAgent

        agents = IastAgent.objects.filter(bind_project_id=1252).values("id")
        from dongtai_common.models.agent_method_pool import MethodPool

        method_pools = MethodPool.objects.filter(agent_id__in=agents).values(
            "req_header_fs"
        )

        from http.server import BaseHTTPRequestHandler

        class HttpRequest(BaseHTTPRequestHandler):
            def __init__(self, raw_request):
                self.body = None
                self.uri = None
                self.params = None
                from io import BytesIO

                self.rfile = BytesIO(raw_request.encode())
                self.raw_requestline = self.rfile.readline()
                self.error_code = self.error_message = None
                self.parse_request()
                self.parse_path()
                self.parse_body()
                self._cookie_keys = set()

            @property
            def cookie_keys(self):
                return self._cookie_keys

            def init_cookie_keys(self):
                cookies = self.headers.get("cookies").split(";")
                for cookie in cookies:
                    self._cookie_keys.add(cookie.strip().split("=")[0])

            def parse_body(self):
                if self.body is None:
                    self.body = self.rfile.read().decode("utf-8")
                return self.body

            def parse_path(self):
                items = self.path.split("?")
                self.uri = items[0]
                self.params = "?".join(items[1:])

        project_headers = set()
        project_cookies = set()
        for method_pool in method_pools:
            try:
                request = HttpRequest(method_pool["req_header_fs"])
                project_headers = project_headers | set(request.headers.keys())
            except BaseException:
                pass
        print(project_headers)
        print(project_cookies)


class MultiUserTestCase(APITestCase):
    def test_update_agent_status_multi_user(self):
        from dongtai_engine.tasks import update_agent_status

        user1 = User.objects.filter(pk=1).get()
        assert user1 is not None
        self.client.force_authenticate(user=user1)
        self.register_agent(name="test1")

        User(id=2, username="test", phone="123456789").save()
        user2 = User.objects.filter(pk=2).get()
        assert user2 is not None
        self.client.force_authenticate(user=user2)
        self.register_agent(name="test2")

        update_agent_status()

    def register_agent(self, **kwargs):
        register_data = REGISTER_JSON
        register_data.update(kwargs)
        data = gzipdata(REGISTER_JSON)
        response = self.client.post(
            "http://testserver/api/v1/agent/register",
            data=data,
            HTTP_CONTENT_ENCODING="gzip",
            content_type="application/json",
        )
        return json.loads(response.content)["data"]


if __name__ == "__main__":
    unittest.main()
