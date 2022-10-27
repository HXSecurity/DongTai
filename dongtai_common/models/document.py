from django.db import models
from dongtai_common.utils.settings import get_managed

from _typeshed import Incomplete
class IastDocument(models.Model):
    title: Incomplete = models.CharField(max_length=100, blank=True, null=True)
    url: Incomplete = models.CharField(max_length=2000, blank=True, null=True)
    language: Incomplete = models.CharField(max_length=100, blank=True, null=True)
    weight: Incomplete = models.IntegerField(default=0)

    class Meta:
        managed: Incomplete = get_managed()
        db_table: str = 'iast_document'
