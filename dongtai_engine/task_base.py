from dongtai_common.models.agent_method_pool import MethodPool
from dongtai_common.models.vulnerablity import IastVulnerabilityModel


def replay_payload_data(relation_ids, replay_type):
    if replay_type == 1:
        vulnerability = IastVulnerabilityModel.objects.filter(id__in=relation_ids).values(
            "id",
            "agent",
            "uri",
            "http_method",
            "http_scheme",
            "req_header",
            "req_params",
            "req_data",
            "taint_value",
            "param_name",
        )
    else:
        vulnerability = MethodPool.objects.filter(id__in=relation_ids).values(
            "id",
            "agent",
            "uri",
            "http_method",
            "http_scheme",
            "req_header",
            "req_params",
            "req_data",
        )
    data = {}
    if vulnerability:
        for item in vulnerability:
            data[item["id"]] = item
    return data
