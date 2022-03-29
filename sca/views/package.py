from sca.models import Package
from django.http import JsonResponse
from rest_framework import views
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from dongtai.endpoint import R, AnonymousAndUserEndPoint

class PackageList(AnonymousAndUserEndPoint):

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
