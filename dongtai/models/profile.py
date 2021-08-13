from django.db import models
import os

class IastProfile(models.Model):
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        managed = True if os.getenv('environment',None) == 'TEST' else False
        db_table = 'iast_profile'
