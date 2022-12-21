from django.test import TestCase
from dongtai_web.threshold.config_setting import get_data_from_dict_by_key
from rest_framework.utils.serializer_helpers import ReturnDict

class TypingTestCase(TestCase):

    def test_typing_in_get_data_from_dict_by_key():
        get_data_from_dict_by_key({"213123132": "123123132"}, ("213123132", ))
        get_data_from_dict_by_key(
            AgentConfigSettingV2TargetSerializer(data={
                "target_type": 1,
                "opt": 1,
                "value": "21313"
            }).data, ("target_type", "opt", "value"))
