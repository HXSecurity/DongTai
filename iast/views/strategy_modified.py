from dongtai.endpoint import R
from dongtai.endpoint import UserEndPoint
from dongtai.models.hook_type import HookType
from dongtai.models.strategy import IastStrategyModel
from iast.utils import extend_schema_with_envcheck, get_response_serializer
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

_ResponseSerializer = get_response_serializer()

class StrategyCreateSerializer(serializers.Serializer):
    vul_name = serializers.CharField(help_text=_('The name of the vulnerability type targeted by the strategy'))
    vul_type = serializers.CharField(help_text=_('Types of vulnerabilities targeted by the strategy'))
    state = serializers.CharField(help_text=_('This field indicates whether the vulnerability is enabled, 1 or 0'))
    vul_desc = serializers.CharField(help_text=_('Description of the corresponding vulnerabilities of the strategy'))
    level_id = serializers.IntegerField(
        help_text=_('The strategy corresponds to the level of vulnerability'))
    vul_fix = serializers.CharField(help_text=_(
        "Suggestions for repairing vulnerabilities corresponding to the strategy"
    ))

class StrategyModified(UserEndPoint):

    @extend_schema_with_envcheck(
        request=StrategyCreateSerializer,
        tags=[_('Strategy')],
        summary=_('Strategy modified'),
        description=_(
            "Get a list of strategies."
        ),
        response_schema=_ResponseSerializer,
    )
    def put(self, request, id_):
        fields = ['vul_name', 'vul_desc', 'vul_fix', 'state','level_id']
        data = {k: v for k, v in request.data.items() if k in fields}
        strategy = IastStrategyModel.objects.filter(
            pk=id_).first()
        HookType.objects.filter(strategy=strategy,type=4).update(name=data['vul_name'])
        HookType.objects.filter(strategy=strategy,type=3).update(name=data['vul_name']+'filter')
        return R.success(data={'id':id_})
        hook_type = HookType.objects.filter(pk=id_).first()
        _update(hook_type, data)
        strategy = IastStrategyModel.objects.filter(
            hook_type=hook_type.id).first()
        if strategy:
            _update(strategy, data)
        return R.success(data={"id": id_})


def _update(model, dic):
    for k, v in dic.items():
        setattr(model, k, v)
    model.save()


def get_model_field(model, exclude=[], include=[]):
    fields = [field.name for field in model._meta.fields]
    if include:
        return [
            include for field in list(set(fields) - set(exclude))
            if field in include
        ]
    return list(set(fields) - set(exclude))
