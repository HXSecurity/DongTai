import unittest

from test import DongTaiTestCase
from django_mock_queries.query import MockSet, MockModel
from dongtai_web.views.api_route_search import _get_hook_type
from dongtai_common.models.vulnerablity import IastVulnerabilityModel
from unittest.mock import patch


@unittest.skip("departured when logic change.")
class TypingTestCase(DongTaiTestCase):
    hooktypes = MockSet(MockModel(pk=1, name=''), )
    strategies = MockSet(MockModel(pk=1, vul_name='strategy'), )
    vul = {"hook_type_id": 1, "strategy_id": 1, "level_id": 1}
    with patch('dongtai_common.models.hook_type.HookType',
               hooktypes), patch('dongtai_common.models.strategy', strategies):
        assert _get_hook_type(vul) is not None
        assert isinstance(_get_hook_type(vul), dict)
