from dongtai.endpoint import R
from dongtai.endpoint import UserEndPoint
from dongtai.models.hook_type import HookType
from dongtai.models.strategy import IastStrategyModel


class StrategyModified(UserEndPoint):

    @extend_schema_with_envcheck(
        tags=[_('Strategy')],
        summary=_('Strategy modified'),
        description=_(
            "Get a list of strategies."
        ),
        response_schema=_ResponseSerializer,
    )
    def put(self, request, id_):
        fields = ['name', 'vul_desc', 'vul_fix', 'enable','level']
        data = {k: v for k, v in request.data.items() if k in fields}
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
