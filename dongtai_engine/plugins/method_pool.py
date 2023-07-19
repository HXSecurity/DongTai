from dongtai_common.models.agent_method_pool import MethodPool
from dongtai_common.models.vulnerablity import IastVulnerabilityModel


def method_pool_after_scan(method_pool: MethodPool):
    pass


def enable_method_pool_post_scan_hook(method_pool: MethodPool) -> bool:
    return not IastVulnerabilityModel.objects.filter(
        method_pool_id=method_pool.id
    ).exists()
