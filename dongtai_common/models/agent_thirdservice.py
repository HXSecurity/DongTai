from django.db import models
from dongtai_common.utils.settings import get_managed
from dongtai_common.models.agent import IastAgent
from dongtai_common.models.project import IastProject


from _typeshed import Incomplete
class IastThirdPartyService(models.Model):
    agent: Incomplete = models.ForeignKey(IastAgent,
                              on_delete=models.CASCADE,
                              db_constraint=False,
                              db_index=True,
                              db_column='agent_id')
    project: Incomplete = models.ForeignKey(IastProject,
                                models.DO_NOTHING,
                                blank=True,
                                default=-1,
                                db_constraint=False)
    address: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    service_type: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    port: Incomplete = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'iast_third_party_service'
