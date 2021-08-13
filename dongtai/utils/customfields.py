######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : customfields
# @created     : Friday Aug 13, 2021 17:34:31 CST
#
# @description :
######################################################################


from django.db.models import CharField


class transCharField(CharField):
    def to_python(self, value):
        return _(super().to_python())
