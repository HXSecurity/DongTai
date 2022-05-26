from django.db import models

from dongtai_common.models import User
from dongtai_common.utils.settings import get_managed


class IastStrategyUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        managed = get_managed()
        db_table = 'iast_strategy_user'
