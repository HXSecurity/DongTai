from django.db import models

from dongtai_common.models import User
from dongtai_common.utils.settings import get_managed


from _typeshed import Incomplete
class IastStrategyUser(models.Model):
    id: Incomplete = models.BigAutoField(primary_key=True)
    name: Incomplete = models.CharField(max_length=200, blank=True, null=True)
    content: Incomplete = models.TextField(blank=True, null=True)
    user: Incomplete = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    status: Incomplete = models.IntegerField(blank=True, null=True)
    created_at: Incomplete = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'iast_strategy_user'
