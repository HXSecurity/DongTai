######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : program_language
# @created     : Tuesday Sep 28, 2021 17:35:55 CST
#
# @description :
######################################################################


from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from dongtai_common.endpoint import AnonymousAndUserEndPoint, R
from dongtai_common.models.program_language import IastProgramLanguage
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer


class IastProgramLanguageSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(help_text=_("The id of program language"))
    name = serializers.CharField(help_text=_("The name of program language"))

    class Meta:
        model = IastProgramLanguage
        fields = ["id", "name"]


_ResponseSerializer = get_response_serializer(
    data_serializer=IastProgramLanguageSerializers(many=True),
)


class ProgrammingLanguageList(AnonymousAndUserEndPoint):
    @extend_schema_with_envcheck(
        tags=[_("Program Language")],
        summary=_("Program Language List"),
        description=_("Get a list of program language."),
        response_schema=_ResponseSerializer,
    )
    def get(self, request):
        queryset = IastProgramLanguage.objects.all()
        return R.success(data=IastProgramLanguageSerializers(queryset, many=True).data)
