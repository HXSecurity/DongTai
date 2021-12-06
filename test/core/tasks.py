import unittest

from test import DongTaiTestCase


class MyTestCase(DongTaiTestCase):
    def test_something(self):
        self.assertEqual(True, False)

    def test_vul_recheck(self):
        from core.tasks import vul_recheck
        vul_recheck()

    def test_search_vul_from_replay_method_pool(self):
        from core.tasks import search_vul_from_replay_method_pool
        method_id = 110
        search_vul_from_replay_method_pool(method_id)

    def test_search_vul_from_method_pool(self):
        method_pool_id = 68871
        from core.tasks import search_vul_from_method_pool
        search_vul_from_method_pool(method_pool_id)

    def test_update_agent_status(self):
        from core.tasks import update_agent_status
        update_agent_status()

    def test_verify_agent_status(self):
        from dongtai.models.agent import IastAgent
        from core.tasks import is_alive
        import time

        timestamp = int(time.time())
        stopped_agents = IastAgent.objects.values("id").filter(is_running=0)
        is_running_agents = list()
        for agent in stopped_agents:
            agent_id = agent['id']
            if is_alive(agent_id=agent_id, timestamp=timestamp):
                is_running_agents.append(agent_id)
            else:
                continue
        if is_running_agents:
            IastAgent.objects.filter(id__in=is_running_agents).update(is_running=1, is_core_running=1)

    def test_update_sca(self):
        from core.tasks import update_sca
        update_sca()


if __name__ == '__main__':
    unittest.main()
