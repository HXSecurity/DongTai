######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : customfields
# @created     : Friday Aug 13, 2021 17:34:31 CST
#
# @description :
######################################################################

from django.db.models import CharField
from functools import wraps
from django.utils.translation import get_language
from collections import defaultdict


def trans_char_field(field, transdict):
    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            value = func(*args, **kwargs)
            try:
                if len(args) > 1:
                    name = args[1]
                else:
                    name = kwargs["name"]
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
