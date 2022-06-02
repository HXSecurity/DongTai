from django.db import models
from dongtai_common.models.agent import IastAgent
from dongtai_common.models.vul_level import IastVulLevel
from dongtai_common.utils.settings import get_managed
from dongtai_common.models.strategy import IastStrategyModel
from dongtai_common.models.hook_type import HookType
class IastVulnerabilityStatus(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        managed = get_managed()
        db_table = 'iast_vulnerability_status'

class IastVulnerabilityModel(models.Model):
    search_keywords = models.CharField(max_length=1000, blank=True, null=True)
    level = models.ForeignKey(IastVulLevel, models.DO_NOTHING, blank=True, null=True)
    url = models.CharField(max_length=2000, blank=True, null=True)
    uri = models.CharField(max_length=255, blank=True, null=True)
    # 模糊搜索 全文索引 查询
    vul_title = models.CharField(max_length=255, blank=True, null=True,default="")
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
    first_time = models.IntegerField(blank=True, null=True)
    latest_time = models.IntegerField(blank=True, null=True)
    latest_time_desc = models.IntegerField(blank=True, null=True, default=0)
    level_id_desc = models.SmallIntegerField(blank=True, null=True, default=0)
    client_ip = models.CharField(max_length=255, blank=True, null=True)
    param_name = models.CharField(max_length=255, blank=True, null=True, default='')
    is_del = models.SmallIntegerField(blank=True, null=True,default=0)
    method_pool_id = models.IntegerField(default=-1, blank=True, null=True)
    strategy = models.ForeignKey(IastStrategyModel,
                                  on_delete=models.DO_NOTHING,
                                  db_constraint=False,
                                  db_column='strategy_id')
    hook_type = models.ForeignKey(HookType,
                                  on_delete=models.DO_NOTHING,
                                  db_constraint=False,
                                  db_column='hook_type_id')
    status = models.ForeignKey(IastVulnerabilityStatus,
                               on_delete=models.DO_NOTHING,
                               db_constraint=False,
                               db_column='status_id')

    class Meta:
        managed = get_managed()
        db_table = 'iast_vulnerability'

    def save(self, *args, **kwargs):
        key_works = [
            # self.uri,
            # self.http_method,
            # self.http_scheme,
            # self.http_protocol,
            # self.top_stack,
            # self.bottom_stack,
            self.strategy.vul_type,
            self.strategy.vul_name,
        ]

        self.search_keywords = " ".join(key_works)
        self.latest_time_desc = -int(self.latest_time)
        self.level_id_desc = -int(self.level_id)
        super(IastVulnerabilityModel, self).save(*args, **kwargs)


