import copy
from functools import wraps

from django.core.cache import cache
from django.utils.translation import gettext_lazy as _
from rest_framework.authentication import TokenAuthentication, get_authorization_header


class DongTaiAppConfigPatch:
    def ready(self):
        try:
            from dongtai_conf.plugin import monkey_patch

            monkey_patch(self.name)
        except ImportError as e:
            print(e)
            pass


class CSPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response[
            "Content-Security-Policy"
        ] = "default-src * ; img-src *;media-src *;script-src 'self' cdn.jsdelivr.net 'unsafe-inline'"
        return response


def make_hash(obj):
    """Make a hash from an arbitrary nested dictionary, list, tuple or
    set.

    """
    if isinstance(obj, list | set | tuple):
        return hash(tuple([make_hash(e) for e in obj]))
    if isinstance(obj, str):
        return hash(tuple(ord(i) for i in obj))
    if not isinstance(obj, dict):
        return hash(obj)

    new_obj = copy.deepcopy(obj)
    for k, v in new_obj.items():
        new_obj[k] = make_hash(v)

    return hash(tuple(frozenset(new_obj.items())))


def cached(
    function,
    random_range: tuple = (50, 100),
    use_celery_update: bool = False,
    cache_logic_none: bool = True,
):
    """Return a version of this function that caches its results for
    the time specified.

    >>> def foo(x): print "called"; return 1
    >>> cached(foo)('whatever')
    called
    1
    >>> cached(foo)('whatever')
    1

    """
    import random

    from dongtai_engine.preheat import function_flush

    @wraps(function)
    def get_cache_or_call(*args, **kwargs):
        # known bug: if the function returns None, we never save it in
        # the cache
        cache_key = make_hash((function.__module__ + function.__name__, args, kwargs))
        cached_result = cache.get(cache_key, "Not such key")
        if random_range:
            cache_time = random.randint(*random_range)
        if use_celery_update:
            function_flush.apply_async(
                args=(
                    function.__module__,
                    function.__name__,
                    cache_time,
                    tuple(args),
                    kwargs,
                )
            )
        if cached_result == "Not such key":
            result = function(*args, **kwargs)
            if cache_logic_none and result is None:
                cache.set(cache_key, result, cache_time)
            else:
                cache.set(cache_key, result, cache_time)
            return result
        if cached_result is None:
            return cached_result
        return cached_result

    get_cache_or_call.__origin__name__ = "cached"
    get_cache_or_call.__random_range__ = random_range
    return get_cache_or_call


def disable_cache(function, args=(), kwargs={}):
    cache_key = make_hash((function.__module__ + function.__name__, args, kwargs))
    cache.delete(cache_key)


def cached_decorator(random_range, use_celery_update=False, cache_logic_none=True):
    def _noname(function):
        return cached(
            function,
            random_range,
            use_celery_update=use_celery_update,
            cache_logic_none=cache_logic_none,
        )

    return _noname


@cached_decorator(random_range=(60, 120), use_celery_update=False)
def get_user_from_department_key(key):
    from dongtai_common.models.department import Department
    from dongtai_common.models.user import User

    department = Department.objects.get(token=key)
    principal = User.objects.filter(pk=department.principal_id).first()
    user = principal if principal else User.objects.filter(pk=1).first()
    user.using_department = department
    return user


class DepartmentTokenAuthentication(TokenAuthentication):
    keyword = "Token GROUP"
    model = None

    def auth_decodedenticate_credentials(self, key):
        from rest_framework import exceptions

        from dongtai_common.models.department import Department

        try:
            user = get_user_from_department_key(key)
        except Department.DoesNotExist:
            raise exceptions.AuthenticationFailed(_("Invalid token."))
        return (user, key)

    def authenticate(self, request):
        auth = get_authorization_header(request)
        if not auth or not auth.lower().startswith(self.keyword.lower().encode()):
            return None
        token = auth.lower().replace(self.keyword.lower().encode(), b"", 1).decode()
        return self.auth_decodedenticate_credentials(token)
