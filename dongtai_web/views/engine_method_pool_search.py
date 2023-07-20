import logging
import operator
import time

from django.db.models import Q
from django.db.utils import OperationalError
from django.utils.translation import gettext_lazy
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from dongtai_common.endpoint import AnonymousAndUserEndPoint, R
from dongtai_common.models.agent import IastAgent
from dongtai_common.models.agent_method_pool import MethodPool
from dongtai_common.models.project import IastProject
from dongtai_common.models.user import User
from dongtai_common.models.vulnerablity import IastVulnerabilityModel
from dongtai_common.utils.const import OPERATE_GET
from dongtai_conf.settings import ELASTICSEARCH_STATE
from dongtai_web.utils import (
    assemble_query,
    assemble_query_2,
    extend_schema_with_envcheck,
    get_model_field,
    get_response_serializer,
)

logger = logging.getLogger("dongtai-webapi")


class MethodPoolSearchProxySer(serializers.Serializer):
    page_size = serializers.IntegerField(min_value=1, help_text=_("number per page"))
    highlight = serializers.IntegerField(
        default=1,
        help_text=_(
            "Whether to enable highlighting, the text where the regular expression matches will be highlighted"
        ),
    )
    exclude_ids = serializers.ListField(
        child=serializers.IntegerField(),
        help_text=_(
            "Exclude the method_pool entry with the following id, this field is used to obtain the data of the entire project in batches."
        ),
        required=False,
    )
    time_range = serializers.ListField(
        child=serializers.IntegerField(min_value=1, help_text=_("time  format such as 1,1628190947242")),
        min_length=2,
        max_length=2,
        help_text=_(
            "Time range, the default is the current time to the previous seven days, separated by',', format such as 1,1628190947242"
        ),
    )
    url = serializers.CharField(
        help_text=_("The url of the method pool, search using regular syntax"),
        required=False,
    )
    res_header = serializers.CharField(
        help_text=_("The response header of the method pood, search using regular syntax"),
        required=False,
    )
    res_body = serializers.CharField(
        help_text=_("The response body of the calling chain, search using regular syntax"),
        required=False,
    )
    req_header_fs = serializers.CharField(
        help_text=_("The request header of the calling chain, search using regular syntax"),
        required=False,
    )
    req_data = serializers.CharField(
        help_text=_("The request data of the calling chain, search using regular syntax"),
        required=False,
    )
    sinkvalues = serializers.CharField(
        help_text=_("The sinkvalues of the calling chain, search using regular syntax"),
        required=False,
    )
    signature = serializers.CharField(
        help_text=_("The signature of the calling chain, search using regular syntax"),
        required=False,
    )
    update_time = serializers.CharField(
        help_text=_(
            "The filter field will return the method call chain with the update time after this time, which can be combined with the exclude_ids field to handle paging"
        ),
        required=False,
    )
    search_mode = serializers.IntegerField(
        help_text=_("the search_mode , 1-contains match ,2-contains not match "),
        default=1,
        required=False,
    )


class MethodPoolSearchResponseRelationVulnerablitySer(serializers.Serializer):
    vulnerablity_type = serializers.CharField()
    vulnerablity_hook_type_id = serializers.IntegerField()
    vulnerablity_id = serializers.IntegerField()
    level_id = serializers.IntegerField()


class MethodPoolSearchResponseMethodPoolSer(serializers.Serializer):
    id = serializers.IntegerField()
    agent_id = serializers.IntegerField()
    url = serializers.CharField()
    uri = serializers.CharField()
    http_method = serializers.CharField()
    http_scheme = serializers.CharField()
    http_protocol = serializers.CharField()
    req_header = serializers.CharField()
    req_header_fs = serializers.CharField()
    req_params = serializers.CharField()
    req_data = serializers.CharField()
    res_header = serializers.CharField()
    res_body = serializers.CharField()
    context_path = serializers.CharField()
    method_pool = serializers.CharField()
    pool_sign = serializers.CharField()
    client_ip = serializers.CharField()
    update_time = serializers.IntegerField()
    create_time = serializers.IntegerField()
    uri_sha1 = serializers.CharField()
    uri_highlight = serializers.CharField()
    res_header_highlight = serializers.CharField()
    res_body_highlight = serializers.CharField()
    req_header_fs_highlight = serializers.CharField()
    req_data_highlight = serializers.CharField()


class MethodPoolSearchResponseRelationSer(serializers.Serializer):
    method_pool_id = serializers.IntegerField()
    agent_id = serializers.IntegerField()
    agent_name = serializers.CharField()
    agent_is_running = serializers.IntegerField()
    project_name = serializers.CharField()
    user_id = serializers.IntegerField()
    user_name = serializers.CharField()
    vulnerablities = MethodPoolSearchResponseRelationVulnerablitySer(many=True)


class MethodPoolSearchResponseAggregationSer(serializers.Serializer):
    method_pool_id = serializers.IntegerField()
    count = serializers.IntegerField()


class MethodPoolSearchResponseAfterkeySer(serializers.Serializer):
    update_time = serializers.IntegerField()


class MethodPoolSearchResponseSer(serializers.Serializer):
    method_pools = MethodPoolSearchResponseMethodPoolSer(many=True)
    relations = MethodPoolSearchResponseRelationSer(many=True)
    aggregation = MethodPoolSearchResponseAggregationSer(many=True)
    afterkeys = MethodPoolSearchResponseAfterkeySer(many=True)


_GetResponseSerializer = get_response_serializer(MethodPoolSearchResponseSer())


class MethodPoolSearchProxy(AnonymousAndUserEndPoint):
    @extend_schema_with_envcheck(
        request=MethodPoolSearchProxySer,
        tags=[_("Method Pool"), OPERATE_GET],
        summary=_("Method Pool Search"),
        description=_(
            "Search for the method pool information according to the following conditions, the default is regular expression input, regular specifications refer to REGEX POSIX 1003.2"
        ),
        response_schema=_GetResponseSerializer,
    )
    def post(self, request):
        page_size = int(request.data.get("page_size", 1))
        request.data.get("page_index", 1)
        highlight = request.data.get("highlight", 1)
        fields = ["url", "res_body"]
        model_fields = ["url", "res_header", "res_body", "req_header_fs", "req_data"]
        fields = get_model_field(
            MethodPool,
            include=model_fields,
        )
        search_after_keys = ["update_time"]
        exclude_ids = request.data.get("exclude_ids", None)
        time_range = request.data.get("time_range", None)
        try:
            search_mode = int(request.data.get("search_mode", 1))
            if page_size <= 0:
                return R.failure(gettext_lazy("Parameter error"))
            [start_time, end_time] = (
                time_range
                if time_range is not None and len(time_range) == 2
                else [
                    int(time.time()) - 60 * 60 * 24 * 7,
                    int(time.time())
                    # and 0 < time_range[1] - time_range[
                    #         0] <= 60 * 60 * 24 * 7 else [
                ]
            )
            ids = exclude_ids if isinstance(exclude_ids, list) and all(isinstance(x, int) for x in exclude_ids) else []
        except BaseException:
            return R.failure(gettext_lazy("Parameter error"))
        search_fields = dict(filter(lambda k: k[0] in fields, request.data.items()))
        search_fields_: list = []
        for k, v in search_fields.items():
            search_fields_.append((k, v))
        search_after_fields = list(
            filter(
                lambda x: x[0] in search_after_keys,
                (
                    (x[0].replace("search_after_", ""), x[1])
                    for x in filter(lambda x: x[0].startswith("search_after_"), request.data.items())
                ),
            )
        )
        q = Q()
        if ELASTICSEARCH_STATE:
            method_pools = search_generate(
                search_fields_,
                time_range,
                self.get_auth_users(request.user).values_list("id", flat=True),
                search_after_fields,
                exclude_ids,
                page_size,
                search_mode,
            )
            method_pools = [i._d_ for i in method_pools]
            for method_pool in method_pools:
                method_pool["req_header_fs"] = method_pool["req_header_for_search"]
            method_pools = list(
                MethodPool.objects.filter(
                    agent_id__in=[i["agent_id"] for i in method_pools],
                    pool_sign__in=[i["pool_sign"] for i in method_pools],
                )
                .order_by("-update_time")
                .values()
                .all()
            )
        else:
            q = assemble_query(search_after_fields, "lte", q, operator.and_)
            if search_mode == 1:
                q = assemble_query(search_fields_, "contains", Q(), operator.or_)
            elif search_mode == 2:
                q = assemble_query_2(search_fields_, "contains", Q(), operator.and_)
            if "id" in request.data:
                q = q & Q(pk=request.data["id"])
            q = q & Q(
                agent_id__in=[item["id"] for item in list(self.get_auth_agents_with_user(request.user).values("id"))]
            )
            if time_range:
                q = q & (Q(update_time__gte=start_time) & Q(update_time__lte=end_time))
            q = (q & (~Q(pk__in=ids))) if ids is not None and ids != [] else q
            queryset = MethodPool.objects.filter(q).order_by("-update_time")[:page_size]
            try:
                method_pools = list(queryset.values().using("timeout10"))
            except OperationalError as e:
                if e.args[0] != 3024:
                    logger.warning(e, exc_info=e)
                else:
                    logger.debug(e, exc_info=e)
                return R.failure(msg="处理超时,建议选择更小的查询时间范围")
        afterkeys = {}
        for i in method_pools[-1:]:
            afterkeys["update_time"] = i["update_time"]
        agents = (
            IastAgent.objects.filter(pk__in=[i["agent_id"] for i in method_pools])
            .all()
            .values("bind_project_id", "token", "id", "user_id", "online")
        )
        projects = IastProject.objects.filter(pk__in=[i["bind_project_id"] for i in agents]).values(
            "id", "name", "user_id"
        )
        vulnerablity = (
            IastVulnerabilityModel.objects.filter(method_pool_id__in=[i["id"] for i in method_pools])
            .all()
            .values(
                "id",
                "hook_type_id",
                "hook_type__name",
                "strategy__vul_name",
                "strategy_id",
                "method_pool_id",
                "level_id",
            )
            .distinct()
        )
        users = User.objects.filter(pk__in=[_["user_id"] for _ in agents]).values("id", "username")
        vulnerablities = list(vulnerablity)
        relations = []
        [agents, projects, users] = _transform([agents, projects, users], "id")
        for method_pool in method_pools:
            item = {}
            item["method_pool_id"] = method_pool["id"]
            agent = agents.get(method_pool["agent_id"], None)
            if agent:
                item["agent_id"] = agent["id"]
                item["agent_name"] = agent["token"]
                item["agent_is_running"] = agent["online"]
                project = projects.get(agent["bind_project_id"], None)
                if project:
                    item["project_id"] = project["id"]
                    item["project_name"] = project["name"]
                user = users.get(agent["user_id"], None)
                if user:
                    item["user_id"] = user["id"]
                    item["user_name"] = user["username"]
            item["vulnerablities"] = []
            for vulnerablity in list(filter(lambda _: _["method_pool_id"] == method_pool["id"], vulnerablities)):
                _ = {}
                type_ = [
                    x
                    for x in [
                        vulnerablity["strategy__vul_name"],
                        vulnerablity["hook_type__name"],
                    ]
                    if x is not None
                ]
                _["vulnerablity_type"] = type_[0] if type_ else ""
                _["vulnerablity_id"] = vulnerablity["id"]
                _["vulnerablity_hook_type_id"] = vulnerablity["hook_type_id"]
                _["level_id"] = vulnerablity["level_id"]
                item["vulnerablities"].append(_)
            relations.append(item)
        aggregation = {}
        aggregation["vulnerablities_count"] = aggregation_count(relations, "method_pool_id", "vulnerablities")
        if highlight:
            for method_pool in method_pools:
                for field in model_fields:
                    if field in search_fields and request.data.get(field, None) and search_mode == 1:
                        if method_pool[field] is None:
                            continue
                        method_pool[f"{field}_highlight"] = highlight_matches(
                            request.data[field], method_pool[field], "<em>{0}</em>"
                        )
                    elif field in fields:
                        if method_pool[field] is None:
                            continue
                        method_pool[f"{field}_highlight"] = method_pool[field].replace("<", "&lt;")
                    else:
                        if method_pool[field] is None:
                            continue
                        method_pool[f"{field}_highlight"] = method_pool[field].replace("<", "&lt;")
        return R.success(
            data={
                "method_pools": method_pools,
                "relations": relations,
                "aggregation": aggregation,
                "afterkeys": afterkeys,
            }
        )


def _transform(models: list, reindex_id: str):
    return [{_[reindex_id]: _ for _ in model} for model in models]


def aggregation_count(list_, primary_key, count_key):
    """
    params
    list_ : [{},{}]
    """
    return [{primary_key: x[primary_key], "count": len(x[count_key])} for x in list_]


def highlight_matches(query, text, html):
    text = text.replace("<", "&lt;")

    def span_matches(match):
        return html.format(match.group(0))

    return text.replace(query, html.format(query))


def search_generate(
    search_fields,
    time_range,
    user_ids,
    search_after_fields,
    filter_ids,
    size,
    search_mode,
):
    from elasticsearch import Elasticsearch
    from elasticsearch_dsl import Q

    from dongtai_common.models.agent_method_pool import MethodPoolDocument

    start_time, end_time = time_range
    must_query = [
        Q("range", update_time={"gte": start_time, "lte": end_time}),
    ]
    must_not_query = [Q("terms", ids=filter_ids)]
    should_query = []
    search_fields = dict(search_fields)
    if "req_header_fs" in search_fields:
        search_fields["req_header_for_search"] = search_fields["req_header_fs"]
        del search_fields["req_header_fs"]
    search_fields = [(k, v) for k, v in dict(search_fields).items()]
    if search_mode == 1:
        should_query = [Q("match", **(dict([search_field]))) for search_field in search_fields]
    elif search_mode == 2:
        must_not_query.extend([Q("match", **(dict([search_field]))) for search_field in search_fields])
    if user_ids:
        must_query.append(Q("terms", user_id=list(user_ids)))
    if search_after_fields:
        must_query.extend(
            [
                Q(
                    "range",
                    **{
                        k: {
                            "gte": v,
                        }
                    },
                )
                for k, v in search_after_fields
            ]
        )
    a = Q(
        "bool",
        must=must_query,
        must_not=must_not_query,
        should=should_query,
        minimum_should_match=1,
    )
    from dongtai_conf import settings

    return list(
        MethodPoolDocument.search()
        .query(a)
        .sort("-update_time")[:size]
        .using(Elasticsearch(settings.ELASTICSEARCH_DSL["default"]["hosts"]))
    )
