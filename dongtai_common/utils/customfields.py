######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : customfields
# @created     : Friday Aug 13, 2021 17:34:31 CST
#
# @description :
######################################################################

from collections import defaultdict
from functools import wraps

from django.db.models import CharField
from django.utils.translation import get_language


def trans_char_field(field, transdict):
    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            value = func(*args, **kwargs)
            try:
                name = args[1] if len(args) > 1 else kwargs["name"]
            except BaseException as e:
                print(e)
                return value
            res = [
                v[value]
                for k, v in transdict.items()
                if name == field and k == get_language() and v.get(value, None)
            ]
            return res[0] if res else value

        return wrapped

    return wrapper
