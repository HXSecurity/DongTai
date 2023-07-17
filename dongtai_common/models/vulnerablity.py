import uuid
from django.core.cache import cache
from django_elasticsearch_dsl.search import Search

from dongtai_common.models.server import IastServer
from dongtai_conf.settings import VULNERABILITY_INDEX
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from django.db import models
from dongtai_common.models.agent import IastAgent
from dongtai_common.models.vul_level import IastVulLevel
from dongtai_common.utils.settings import get_managed
from dongtai_common.models.strategy import IastStrategyModel
from dongtai_common.models.hook_type import HookType
from dongtai_common.models.project import IastProject
from dongtai_common.models.project_version import IastProjectVersion
import logging


logger = logging.getLogger('dongtai-core')

class IastVulnerabilityStatus(models.Model):
    name = models.CharField(max_length=100, blank=True)

    class Meta:
        managed = get_managed()
        db_table = 'iast_vulnerability_status'


class IastVulnerabilityModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    search_keywords = models.CharField(max_length=1000, blank=True)
    level = models.ForeignKey(IastVulLevel,
                              models.DO_NOTHING,
                              blank=True)
    url = models.CharField(max_length=2000, blank=True)
    uri = models.CharField(max_length=255, blank=True)
    pattern_uri = models.CharField(max_length=255, blank=True, null=True)
    # 模糊搜索 全文索引 查询
    vul_title = models.CharField(max_length=255,
                                 blank=True,
                                 default="")
    http_method = models.CharField(max_length=10, blank=True)
    http_scheme = models.CharField(max_length=255, blank=True)
    http_protocol = models.CharField(max_length=255, blank=True)
    req_header = models.TextField(blank=True)
    req_params = models.CharField(max_length=2000,
                                  blank=True,
                                  default="")
    req_data = models.TextField(blank=True, )
    res_header = models.TextField(blank=True)
    res_body = models.TextField(blank=True)
    full_stack = models.TextField(blank=True, null=True)
    top_stack = models.CharField(max_length=255, blank=True, null=True)
    bottom_stack = models.CharField(max_length=255, blank=True, null=True)
    taint_value = models.CharField(max_length=255, blank=True, null=True)
    taint_position = models.CharField(max_length=255, blank=True, null=True)
    agent = models.ForeignKey(IastAgent,
                              models.DO_NOTHING,
                              blank=True)
    language = models.CharField(max_length=10, blank=True, null=True)
    context_path = models.CharField(max_length=255, blank=True)
    counts = models.IntegerField(blank=True)
    first_time = models.IntegerField(blank=True)
    latest_time = models.IntegerField(blank=True)
    latest_time_desc = models.IntegerField(blank=True, default=0)
    level_id_desc = models.SmallIntegerField(blank=True, default=0)
    client_ip = models.CharField(max_length=255, blank=True)
    param_name = models.CharField(max_length=255,
                                  blank=True,
                                  null=True)
    is_del = models.SmallIntegerField(blank=True, default=0)
    method_pool_id = models.IntegerField(default=-1, blank=True)
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
                               db_column='status_id',
                               null=True)
    project = models.ForeignKey(IastProject,
                                on_delete=models.CASCADE,
                                blank=True,
                                default=-1)
    project_version = models.ForeignKey(IastProjectVersion,
                                        on_delete=models.CASCADE,
                                        blank=True,
                                        default=-1)
    server = models.ForeignKey(IastServer,
                               on_delete=models.CASCADE,
                               blank=True,
                               default=-1)

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
        if not self.pattern_uri:
            self.pattern_uri = self.pattern_uri
        self.search_keywords = " ".join(key_works)
        try:
            self.latest_time_desc = -int(self.latest_time)
            self.level_id_desc = -int(self.level_id)
        except TypeError as e:
            logger.error(
                "level_id: {self.level_id} latest_time: {self.latest_time}",
                exc_info=e)
        super(IastVulnerabilityModel, self).save(*args, **kwargs)


@registry.register_document
class IastVulnerabilityDocument(Document):
    user_id = fields.IntegerField(attr="agent.user_id")
    agent_id = fields.IntegerField(attr="agent_id")
    strategy_id = fields.IntegerField(attr="strategy_id")
    hook_type_id = fields.IntegerField(attr="hook_type_id")
    status_id = fields.IntegerField(attr="status_id")
    level_id = fields.IntegerField(attr="level_id")
    bind_project_id = fields.IntegerField(attr="agent.bind_project_id")
    # language = fields.IntegerField(attr="agent.language")
    project_version_id = fields.IntegerField(attr="agent.project_version_id")
    project_name = fields.IntegerField(attr="agent.bind_project.name")
    token = fields.IntegerField(attr="agent.token")
    server_id = fields.IntegerField(attr="server_id")
    department_id = fields.IntegerField(attr="agent.department_id")

    @classmethod
    def search(cls, using=None, index=None):
        uuid_key = uuid.uuid4().hex
        cache_uuid_key = cache.get_or_set(
            f'es-documents-shards-{cls.__name__}', uuid_key, 60 * 1)
        return Search(using=cls._get_using(using),
                      index=cls._default_index(index),
                      doc_type=[cls],
                      model=cls.django.model).params(preference=cache_uuid_key)

    def get_instances_from_related(self, related_instance):
        """If related_models is set, define how to retrieve the Car instance(s) from the related model.
        The related_models option should be used with caution because it can lead in the index
        to the updating of a lot of items.
        """
        if isinstance(related_instance, IastAgent):
            if related_instance.bind_project_id < 0:
                return related_instance.iastvulnerabilitymodel_set.all()

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
            'method_pool_id', 'language',
        ]
        auto_refresh = False

        ignore_signals = False
