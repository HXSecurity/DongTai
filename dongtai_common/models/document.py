from django.db import models
from dongtai_common.utils.settings import get_managed


class IastDocument(models.Model):
    title = models.CharField(max_length=100, blank=True)
    url = models.CharField(max_length=2000, blank=True)
    language = models.CharField(max_length=100, blank=True)
    weight = models.IntegerField(default=0)

    class Meta:
        managed = get_managed()
        db_table = 'iast_document'
