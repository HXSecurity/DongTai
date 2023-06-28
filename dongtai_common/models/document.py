from django.db import models
from dongtai_common.utils.settings import get_managed


class IastDocument(models.Model):
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=2000)
    language = models.CharField(max_length=100)
    weight = models.IntegerField(default=0)

    class Meta:
        managed = get_managed()
        db_table = 'iast_document'
