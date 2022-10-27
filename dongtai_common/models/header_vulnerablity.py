from django.db import models
from dongtai_common.models.agent import IastAgent
from dongtai_common.models.vul_level import IastVulLevel
from dongtai_common.utils.settings import get_managed
from dongtai_common.models.strategy import IastStrategyModel
from dongtai_common.models.hook_type import HookType
from dongtai_common.models.server import IastServer
from dongtai_common.models.project import IastProject
from dongtai_common.models.project_version import IastProjectVersion
from dongtai_common.models.agent_method_pool import MethodPool
from dongtai_common.models.vulnerablity import IastVulnerabilityModel


from _typeshed import Incomplete
class IastHeaderVulnerability(models.Model):
    id: Incomplete = models.BigAutoField(primary_key=True)
    project: Incomplete = models.ForeignKey(IastProject,
                                on_delete=models.DO_NOTHING,
                                blank=True,
                                null=True,
                                default=-1,
                                db_constraint=False)
    project_version: Incomplete = models.ForeignKey(IastProjectVersion,
                                        on_delete=models.DO_NOTHING,
                                        blank=True,
                                        null=True,
                                        default=-1,
                                        db_constraint=False)
    url: Incomplete = models.CharField(max_length=255, default='', blank=True, null=True)
    vul: Incomplete = models.ForeignKey(IastVulnerabilityModel,
                            on_delete=models.DO_NOTHING,
                            blank=True,
                            null=True,
                            default=-1,
                            db_constraint=False)

    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'iast_header_vulnerability'


class IastHeaderVulnerabilityDetail(models.Model):
    req_header: Incomplete = models.TextField(
        blank=True,
        null=True,
    )
    res_header: Incomplete = models.TextField(blank=True, null=True)
    agent: Incomplete = models.ForeignKey(IastAgent,
                              models.DO_NOTHING,
                              blank=True,
                              null=True,
                              db_constraint=False)
    method_pool: Incomplete = models.ForeignKey(MethodPool,
                                    models.DO_NOTHING,
                                    blank=True,
                                    null=True,
                                    db_constraint=False)
    header_vul: Incomplete = models.ForeignKey(IastHeaderVulnerability,
                                   models.DO_NOTHING,
                                   blank=True,
                                   null=True,
                                   db_constraint=False)

    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'iast_header_vulnerability_detail'
