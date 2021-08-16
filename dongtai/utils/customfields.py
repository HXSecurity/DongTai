######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : customfields
# @created     : Friday Aug 13, 2021 17:34:31 CST
#
# @description :
######################################################################

from django.db.models import CharField
from django.utils.translation import gettext_lazy as _


def trans_char_field(translist: list) -> CharField:
    class transCharField(CharField):
        def to_python(self, value):
            value = super().to_python(value)
            return _(list(
                filter(lambda x: x == value,
                       translist))[0]) if value in translist else value
    return transCharField
