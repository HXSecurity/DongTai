from django.db import models

class IastProfile(models.Model):
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'iast_profile'
