import logging

from dongtai_common.models import User
from dongtai_web.dongtai_sca.models import Package
from django.http import JsonResponse
from rest_framework import views
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from dongtai_common.endpoint import R, AnonymousAndUserEndPoint, UserEndPoint
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema

from dongtai_web.dongtai_sca.utils import get_asset_id_by_aggr_id

logger = logging.getLogger(__name__)


class PackageList(AnonymousAndUserEndPoint):

    @extend_schema(
        tags=[_('Component')],
        summary="组件列表",
        deprecated=True,
    )
    def get(self, request):
        filter_fields = ['hash', 'aql', 'ecosystem', 'name', 'version']
        _filter = Package.objects.filter().order_by("-updated_at")
        kwargs = {}
        for filter_field in filter_fields:
            _val = request.GET.get(filter_field, "")
            if _val != "":
                kwargs[filter_field] = request.GET.get(filter_field, "")
        _filter = _filter.filter(**kwargs)

        page = int(request.GET.get("page", 1))
        page_size = int(request.GET.get("page_size", 5))

        pageinfo = Paginator(_filter, per_page=page_size)
        result = {
            'data': [],
            'msg': 'success',
            'page': {
                'alltotal': pageinfo.count,
                'num_pages': pageinfo.num_pages,
                'page_size': pageinfo.per_page,
            },
            'status': 201
        }
        if page == 0 or page <= pageinfo.num_pages:
            rows = pageinfo.page(page).object_list

            for row in rows:
                result['data'].append(model_to_dict(row))

        return JsonResponse(result)


class AssetAggrDetailAssetIds(UserEndPoint):
    name = "api-v1-sca-aggr-assets"
    description = ""

    @extend_schema(
        tags=[_('Component')],
        summary="组件详情",
        deprecated=True,
    )
    def get(self, request, aggr_id):
        try:
            auth_users = self.get_auth_users(request.user)
            asset_queryset = self.get_auth_assets(auth_users)

            asset_ids = []
            for asset in asset_queryset:
                asset_ids.append(asset.id)
            asset_ids = get_asset_id_by_aggr_id(aggr_id, asset_ids)

            return R.success(data=asset_ids)
        except Exception as e:
            logger.error(e)
            return R.failure(msg=_('Component asset id query failed'))
