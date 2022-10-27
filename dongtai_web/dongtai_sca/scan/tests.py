from .utils import get_package_vul, get_package

from django.test import TestCase


from .utils import get_latest_version as get_latest_version, get_nearest_version as get_nearest_version, get_package as get_package, get_package_vul as get_package_vul, update_one_sca as update_one_sca
from _typeshed import Incomplete
class ExtenalApiTestCase(TestCase):

    def test_get_package_vul_by_aql(self) -> None:
        res = get_package_vul(
            aql="maven:com.fasterxml.jackson.core:jackson-databind:2.9.3:")
        assert isinstance(res, list)

    def test_get_package_by_ecosystem_and_hash_java(self) -> None:
        res = get_package(
            ecosystem="maven",
            package_hash="3490508379d065fe3fcb80042b62f630f7588606")
        assert isinstance(res, list)

    def test_get_package_by_ecosystem_and_hash_go(self) -> None:
        res = get_package(
            ecosystem="golang",
            package_hash="3c61e56652c8d48ba09390f1170cf868007e1293")
        assert isinstance(res, list)


from test import DongTaiTestCase
from test.apiserver.test_agent_base import AgentTestCase
from .utils import update_one_sca

from .utils import get_nearest_version, get_latest_version


class DongTaiVersionTestCase(TestCase):
    version_list: Incomplete = [
        '1.0', '1.0-m4', '1.0-rc1', '1.0.1', '1.2', '1.2-rc1', '1.2-rc2',
        '1.2.1', '1.2.2', '1.2.3', '1.2.4', '1.2.5', '1.2.6', '1.2.7', '1.2.8',
        '1.2.9', '2.0', '2.0-m1', '2.0-m2', '2.0-m4', '2.0.1', '2.0.2',
        '2.0.3', '2.0.4', '2.0.5', '2.0.6', '2.0.7', '2.0.8', '2.5', '2.5.1',
        '2.5.2', '2.5.3', '2.5.4', '2.5.5', '2.5.6', '2.5.6.SEC01',
        '2.5.6.SEC02', '2.5.6.SEC03', '3.0.0.RELEASE', '3.0.1.RELEASE',
        '3.0.2.RELEASE', '3.0.3.RELEASE', '3.0.4.RELEASE', '3.0.5.RELEASE',
        '3.0.6.RELEASE', '3.0.7.RELEASE', '3.1.0.RELEASE', '3.1.1.RELEASE',
        '3.1.2.RELEASE', '3.1.3.RELEASE', '3.1.4.RELEASE', '3.2.0.RELEASE',
        '3.2.1.RELEASE', '3.2.10.RELEASE', '3.2.11.RELEASE', '3.2.12.RELEASE',
        '3.2.13.RELEASE', '3.2.14.RELEASE', '3.2.15.RELEASE', '3.2.16.RELEASE',
        '3.2.17.RELEASE', '3.2.18.RELEASE', '3.2.2.RELEASE', '3.2.3.RELEASE',
        '3.2.4.RELEASE', '3.2.5.RELEASE', '3.2.6.RELEASE', '3.2.7.RELEASE',
        '3.2.8.RELEASE', '3.2.9.RELEASE', '4.0.0.RELEASE', '4.0.1.RELEASE',
        '4.0.2.RELEASE', '4.0.3.RELEASE', '4.0.4.RELEASE', '4.0.5.RELEASE',
        '4.0.6.RELEASE', '4.0.7.RELEASE', '4.0.8.RELEASE', '4.0.9.RELEASE',
        '4.1.0.RELEASE', '4.1.1.RELEASE', '4.1.2.RELEASE', '4.1.3.RELEASE',
        '4.1.4.RELEASE', '4.1.5.RELEASE', '4.1.6.RELEASE', '4.1.7.RELEASE',
        '4.1.8.RELEASE', '4.1.9.RELEASE', '4.2.0.RELEASE', '4.2.1.RELEASE',
        '4.2.2.RELEASE', '4.2.3.RELEASE', '4.2.4.RELEASE', '4.2.5.RELEASE',
        '4.2.6.RELEASE', '4.2.7.RELEASE', '4.2.8.RELEASE', '4.2.9.RELEASE',
        '4.3.0.RELEASE', '4.3.1.RELEASE', '4.3.10.RELEASE', '4.3.11.RELEASE',
        '4.3.12.RELEASE', '4.3.13.RELEASE', '4.3.14.RELEASE', '4.3.15.RELEASE',
        '4.3.16.RELEASE', '4.3.17.RELEASE', '4.3.18.RELEASE', '4.3.19.RELEASE',
        '4.3.2.RELEASE', '4.3.20.RELEASE', '4.3.21.RELEASE', '4.3.22.RELEASE',
        '4.3.23.RELEASE', '4.3.24.RELEASE', '4.3.25.RELEASE', '4.3.26.RELEASE',
        '4.3.27.RELEASE', '4.3.28.RELEASE', '4.3.29.RELEASE', '4.3.3.RELEASE',
        '4.3.30.RELEASE', '4.3.4.RELEASE', '4.3.5.RELEASE', '4.3.6.RELEASE',
        '4.3.7.RELEASE', '4.3.8.RELEASE', '4.3.9.RELEASE', '5.0.0.RELEASE',
        '5.0.1.RELEASE', '5.0.10.RELEASE', '5.0.11.RELEASE', '5.0.12.RELEASE',
        '5.0.13.RELEASE', '5.0.14.RELEASE', '5.0.15.RELEASE', '5.0.16.RELEASE',
        '5.0.17.RELEASE', '5.0.18.RELEASE', '5.0.19.RELEASE', '5.0.2.RELEASE',
        '5.0.20.RELEASE', '5.0.3.RELEASE', '5.0.4.RELEASE', '5.0.5.RELEASE',
        '5.0.6.RELEASE', '5.0.7.RELEASE', '5.0.8.RELEASE', '5.0.9.RELEASE',
        '5.1.0.RELEASE', '5.1.1.RELEASE', '5.1.10.RELEASE', '5.1.11.RELEASE',
        '5.1.12.RELEASE', '5.1.13.RELEASE', '5.1.14.RELEASE', '5.1.15.RELEASE',
        '5.1.16.RELEASE', '5.1.17.RELEASE', '5.1.18.RELEASE', '5.1.19.RELEASE',
        '5.1.2.RELEASE', '5.1.20.RELEASE', '5.1.3.RELEASE', '5.1.4.RELEASE',
        '5.1.5.RELEASE', '5.1.6.RELEASE', '5.1.7.RELEASE', '5.1.8.RELEASE',
        '5.1.9.RELEASE', '5.2.11.RELEASE', '5.2.19.RELEASE', '5.2.3.RELEASE',
        '5.2.8.RELEASE', '5.3.14', '5.3.15', '5.3.16', '5.3.19'
    ]

    def test_nearest_version(self) -> None:
        version = '5.1.3.RELEASE'
        nrversion = get_nearest_version(version, self.version_list)
        assert nrversion == '5.1.3.RELEASE'

    def test_latest_version(self) -> None:
        assert '5.3.19' == get_latest_version(self.version_list)

    def test_nearest_version_1(self) -> None:
        version = '0.0.1'
        nrversion = get_nearest_version(version, self.version_list)
        assert nrversion == '1.0-rc1'

    def test_nearest_version_2(self) -> None:
        version = '10.0.1'
        nrversion = get_nearest_version(version, self.version_list)
        assert nrversion == ''


from dongtai_common.models.asset import Asset

class AgentHardencodeTestCase(AgentTestCase):

    def test_update_one_sca_java(self) -> None:
        update_one_sca(
            self.agent_id,
            "/Users/xxx/spring-boot/2.3.2.RELEASE/org.springframework:spring-beans.jar",
            "3490508379d065fe3fcb80042b62f630f7588606",
            "org.springframework:spring-beans.jar", "SHA-1")

    def test_update_one_sca_golang(self) -> None:
        update_one_sca(self.agent_id, "pypi:markupsafe:2.0.1:",
                       "a4bb5ffad5564e4a0e25955e3a40b1c6158385b2",
                       "org.springframework:spring-beans.jar", "SHA-1")

    def test_get_package_edge_case(self) -> None:
        update_one_sca(self.agent_id, "",
                       "9b7860a324f4b2f2bc31bcdd99c7ee51fe32e0c8",
                       " org.springframework:spring-web.jar ", "SHA-1")
        asset = Asset.objects.filter(
            agent_id=self.agent_id,
            signature_value="9b7860a324f4b2f2bc31bcdd99c7ee51fe32e0c8").first(
        )

    def test_get_package_edge_case_1(self) -> None:
        update_one_sca(self.agent_id, "",
                       "07b6bf82cea13570b5290d6ed841283a1fcce170",
                       " org.springframework:spring-web.jar ", "SHA-1")
        asset = Asset.objects.filter(
            agent_id=self.agent_id,
            signature_value="07b6bf82cea13570b5290d6ed841283a1fcce170").first(
        )
        assert asset is not None
        assert asset.safe_version_list is not None
        assert asset.iastvulassetrelation_set.all() != []
    
    def test_update_one_sca_java_result_search(self) -> None:
        update_one_sca(
            self.agent_id,
            "/Users/xxx/spring-boot/2.3.2.RELEASE/org.springframework:spring-beans.jar",
            "3490508379d065fe3fcb80042b62f630f7588606",
            "org.springframework:spring-beans.jar", "SHA-1")
        asset = Asset.objects.filter(
            agent_id=self.agent_id,
            signature_value="3490508379d065fe3fcb80042b62f630f7588606").first(
        )
        for i in asset.iastvulassetrelation_set.all():
            assert len(i.vul_dependency_path) > 0
