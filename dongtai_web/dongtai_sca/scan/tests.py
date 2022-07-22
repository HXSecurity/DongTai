from .utils import get_package_vul, get_package

from django.test import TestCase


class ExtenalApiTestCase(TestCase):

    def test_get_package_vul_by_aql(self):
        res = get_package_vul(
            aql="maven:com.fasterxml.jackson.core:jackson-databind:2.9.3:")
        assert isinstance(res, list)

    def test_get_package_by_ecosystem_and_hash_java(self):
        res = get_package(
            ecosystem="maven",
            package_hash="ef9012cf77810f8051d10e616d7ce82f4bd45bb8")
        assert isinstance(res, list)

    def test_get_package_by_ecosystem_and_hash_go(self):
        res = get_package(
            ecosystem="golang",
            package_hash="3c61e56652c8d48ba09390f1170cf868007e1293")
        assert isinstance(res, list)


from test import DongTaiTestCase
from test.apiserver.test_agent_base import AgentTestCase
from .utils import update_one_sca


class AgentHardencodeTestCase(AgentTestCase):

    def test_update_one_sca_java(self):
        update_one_sca(
            self.agent_id,
            "/Users/xxx/spring-boot/2.3.2.RELEASE/org.springframework:spring-beans.jar",
            "a4bb5ffad5564e4a0e25955e3a40b1c6158385b2",
            "org.springframework:spring-beans.jar", "SHA-1")
    
    def test_update_one_sca_golang(self):
        update_one_sca(
            self.agent_id,
            "pypi:markupsafe:2.0.1:",
            "a4bb5ffad5564e4a0e25955e3a40b1c6158385b2",
            "org.springframework:spring-beans.jar", "SHA-1")
