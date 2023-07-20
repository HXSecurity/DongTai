from django.core.cache import cache


class ListPageMaker:
    def parse_args(self, request):
        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("pageSize", 20))
        page_size = page_size if page_size < 50 else 50
        return page, page_size, request.user

    def make_key(self, request, keyName="logs"):
        self.cache_key = f"{request.user.id}_total_{keyName}_id"
        self.cache_key_max_id = f"{request.user.id}_max_{keyName}_id"

    def get_query_cache(self):
        total = cache.get(self.cache_key)
        max_id = cache.get(self.cache_key_max_id)
        return total, max_id

    def set_query_cache(self, queryset):
        total = queryset.values("id").count()
        max_id = queryset.values_list("id", flat=True).order_by("-action_time")[0]
        cache.set(self.cache_key, total, 60 * 60)
        cache.set(self.cache_key_max_id, max_id, 60 * 60)
        return total, max_id
