from django.db import models

class IastDocument(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    url = models.CharField(max_length=100, blank=True, null=True)
    language = models.CharField(max_length=100, blank=True, null=True)
    weight = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'iast_document'
