# Create your tests here.
from django.test import TestCase
from dongtai_web.views.agents_v2 import query_agent
from dongtai_web.views.log_download import (file_newest_N_file_under_path, getzipfilesinmemorty, )
from dongtai_web.views.agents_v2 import (
    query_agent, )

from dongtai_web.threshold.config_setting import (convert_choices_to_dict,
                                                  convert_choices_to_value_dict,
                                                  get_metric_types, get_targets)
from dongtai_common.models.agent_config import (
    IastCircuitTarget,
    IastCircuitConfig,
    IastCircuitMetric,
    TargetType,
    TargetOperator,
    DealType,
    MetricType,
    MetricGroup,
    MetricOperator,
)

class DashboardTestCase(TestCase):
    def test_query_agent(self):
        res = query_agent()
        print(res)


class DashboardTestCase(TestCase):

    def test_findnewest_file(self):
        res = file_newest_N_file_under_path('./dongtai_web', 2)
        print(res)

    def test_getzipfilesinmemorty(self):
        res = getzipfilesinmemorty(['./README.md', './lingzhi.sh'])
        print(res)

    def test_get_zip_together(self):
        from dongtai_web.views.log_download import get_zip_together
        res = get_zip_together([1, 2, 3], 1)
        print(res)

class ChoiceConvertTestCase(TestCase):
    def test_choice_convert(self):
        able_to_search = (MetricType, MetricGroup,
                          TargetOperator,
                          MetricOperator)
        for i in able_to_search:
            res = convert_choices_to_dict(i)
            print(res)
    def test_choice_convert_value(self):
        able_to_search = (MetricType, MetricGroup,
                          TargetOperator,
                          MetricOperator)
        for i in able_to_search:
            res = convert_choices_to_value_dict(i)
            print(res)

    def test_metric_string_concate(self):
        metrics = [{
            "metric_type": 1,
            "opt": 5,
            "value": 100
        }, {
            "metric_type": 2,
            "opt": 5,
            "value": 100
        }, {
            "metric_type": 3,
            "opt": 5,
            "value": 1000000000
        }]
        res = get_metric_types(metrics)
        print(res)
