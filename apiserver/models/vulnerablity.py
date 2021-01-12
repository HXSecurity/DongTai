from django.db import models

from apiserver.models.agent import IastAgent
from apiserver.models.vul_level import IastVulLevel
from user.models import User


class IastVulnerabilityModel(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    level = models.ForeignKey(IastVulLevel, models.DO_NOTHING, blank=True, null=True)
    url = models.CharField(max_length=2000, blank=True, null=True)
    uri = models.CharField(max_length=255, blank=True, null=True)
    http_method = models.CharField(max_length=10, blank=True, null=True)
    http_scheme = models.CharField(max_length=255, blank=True, null=True)
    http_protocol = models.CharField(max_length=255, blank=True, null=True)
    req_header = models.TextField(blank=True, null=True)
    req_params = models.CharField(max_length=2000, blank=True, null=True)
    req_data = models.TextField(blank=True, null=True)
    res_header = models.TextField(blank=True, null=True)
    res_body = models.TextField(blank=True, null=True)
    full_stack = models.TextField(blank=True, null=True)
    top_stack = models.CharField(max_length=255, blank=True, null=True)
    bottom_stack = models.CharField(max_length=255, blank=True, null=True)
    taint_value = models.CharField(max_length=255, blank=True, null=True)
    taint_position = models.CharField(max_length=255, blank=True, null=True)
    agent = models.ForeignKey(IastAgent, models.DO_NOTHING, blank=True, null=True)
    context_path = models.CharField(max_length=255, blank=True, null=True)
    counts = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    language = models.CharField(max_length=255, blank=True, null=True)
    first_time = models.IntegerField(blank=True, null=True)
    latest_time = models.IntegerField(blank=True, null=True)
    client_ip = models.CharField(max_length=255, blank=True, null=True)
    param_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'iast_vulnerability'
