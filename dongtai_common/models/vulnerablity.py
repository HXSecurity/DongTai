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
    req_params = models.CharField(max_length=2000, blank=True, null=True, default="")
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


from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from django_elasticsearch_dsl import Document, fields
from dongtai_conf.settings import VULNERABILITY_INDEX 


@registry.register_document
class IastVulnerabilityDocument(Document):
    user_id = fields.IntegerField(attr="agent.user_id")
    agent_id = fields.IntegerField(attr="agent_id")
    strategy_id = fields.IntegerField(attr="strategy_id")
    hook_type_id = fields.IntegerField(attr="hook_type_id")
    status_id = fields.IntegerField(attr="status_id")
    level_id = fields.IntegerField(attr="level_id")
    bind_project_id = fields.IntegerField(attr="agent.bind_project_id")
    language = fields.IntegerField(attr="agent.language")
    project_version_id = fields.IntegerField(
        attr="agent.bind_project_version_id")
    project_name = fields.IntegerField(attr="agent.bind_project.name")
    token = fields.IntegerField(attr="agent.token")

    class Index:
        name = VULNERABILITY_INDEX

    class Django:
        model = IastVulnerabilityModel
        fields = [
            'id', 'search_keywords', 'url', 'uri', 'vul_title', 'http_method',
            'http_scheme', 'http_protocol', 'req_header', 'req_params',
            'req_data', 'res_header', 'res_body', 'full_stack', 'top_stack',
            'bottom_stack', 'taint_value', 'taint_position', 'context_path',
            'counts', 'first_time', 'latest_time', 'latest_time_desc',
            'level_id_desc', 'client_ip', 'param_name', 'is_del',
            'method_pool_id'
        ]

        ignore_signals = False
