import unittest

from test import DongTaiTestCase


class AgentDownloadTestCase(DongTaiTestCase):
    def test_something(self):
        self.assertEqual(True, False)

    def test_python_agent_download(self):
        pass

    def test_python_agent_replace_config(self):
        from apiserver.views.agent_download import PythonAgentDownload
        download_handler = PythonAgentDownload()
        download_handler.replace_config()


if __name__ == '__main__':
    unittest.main()
