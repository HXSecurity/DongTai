from rest_framework.request import Request

from dongtai.endpoint import R
from dongtai.endpoint import UserEndPoint
from dongtai.models.strategy_user import IastStrategyUser
from dongtai.models.strategy import IastStrategyModel


class StrategyModified(UserEndPoint):

    def put(self, request):
        '''
        用户修改策略
        '''
        id_ = request.data.get("id", None)
        # 策略名称
        strategy = IastStrategyModel.objects.filter(
            pk=id_, user_id=request.user.id).first()
        dic = {}
        _update(strategy, dic)
        return R.success(data={"id": id_})


def _update(strategy, dic):
    for k, v in dic.items():
        setattr(strategy, k, v)
    strategy.save()
