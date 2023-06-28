from django.db import models
from dongtai_common.models.agent import IastAgent
from dongtai_common.utils.settings import get_managed
from dongtai_common.models.project import IastProject
from dongtai_common.models.project_version import IastProjectVersion
from dongtai_common.models.agent_method_pool import MethodPool
from dongtai_common.models.vulnerablity import IastVulnerabilityModel


class IastHeaderVulnerability(models.Model):
    id = models.BigAutoField(primary_key=True)
    project = models.ForeignKey(IastProject,
                                on_delete=models.DO_NOTHING,
                                default=-1,
                                db_constraint=False)
    project_version = models.ForeignKey(IastProjectVersion,
                                        on_delete=models.DO_NOTHING,
                                        default=-1,
                                        db_constraint=False)
    url = models.CharField(max_length=255, default='')
    vul = models.ForeignKey(IastVulnerabilityModel,
                            on_delete=models.DO_NOTHING,
                            default=-1,
                            db_constraint=False)

    class Meta:
        managed = get_managed()
        db_table = 'iast_header_vulnerability'


class IastHeaderVulnerabilityDetail(models.Model):
    req_header = models.TextField()
    res_header = models.TextField(blank=True)
    agent = models.ForeignKey(IastAgent,
                              models.DO_NOTHING,
                              db_constraint=False)
    method_pool = models.ForeignKey(MethodPool,
                                    models.DO_NOTHING,
                                    db_constraint=False)
    header_vul = models.ForeignKey(IastHeaderVulnerability,
                                   models.DO_NOTHING,
                                   blank=True,
                                   db_constraint=False)

    class Meta:
        managed = get_managed()
        db_table = 'iast_header_vulnerability_detail'
