from dongtai.utils import const
from dongtai.models.hook_type import HookType
from dongtai.models.strategy import IastStrategyModel
from dongtai.models.document import IastDocument

from dongtai.endpoint import R
from dongtai.utils import const
from dongtai.endpoint import UserEndPoint
from iast.serializers.strategy import StrategySerializer
from django.forms.models import model_to_dict


class DocumentsEndpoint(UserEndPoint):
    def get(self, request):
        page_size = request.GET.get('page_size', 100)
        page = request.GET.get('page', 1)

        page_summary, documents = self.get_paginator(IastDocument.objects.all(), page,
                                                     page_size)
        return R.success(
                data={'documents':[model_to_dict(document) for document in documents]})
