import unittest

from test import DongTaiTestCase


class AgentDownloadTestCase(DongTaiTestCase):
    def test_something(self):
        self.assertEqual(True, False)

    def test_python_agent_download(self):
        pass

    def test_python_agent_replace_config(self):
        from dongtai_protocol.views.agent_download import PythonAgentDownload
        download_handler = PythonAgentDownload(user_id=1)
        download_handler.replace_config()

    def test_java_agent_download(self):
        from dongtai_protocol.views.agent_download import JavaAgentDownload
        download_handler = JavaAgentDownload(user_id=1)
        download_handler.download_agent()


if __name__ == '__main__':
    unittest.main()
