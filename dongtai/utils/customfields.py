######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : customfields
# @created     : Friday Aug 13, 2021 17:34:31 CST
#
# @description :
######################################################################

from django.db.models import CharField
from django.utils.translation import gettext_lazy as _
from functools import wraps


def trans_char_field(field, translist):
    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            value = func(*args, **kwargs)
            try:
                if len(args) > 2:
                    name = args[1]
                else:
                    name = kwargs['name']
                print(name)
            except BaseException as e:
                print(e)
                return value
            return _(list(filter(lambda x: x == value, translist))
                     [0]) if value in translist and name == field else value
        return wrapped
    return wrapper
