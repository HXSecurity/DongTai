######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : sensitive_info_rule
# @created     : 星期三 11月 17, 2021 16:15:57 CST
#
# @description : 
######################################################################



import logging

from dongtai.endpoint import UserEndPoint, R
from dongtai.models.hook_type import HookType
from dongtai.utils import const

from iast.serializers.hook_type_strategy import HookTypeSerialize
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from iast.utils import extend_schema_with_envcheck, get_response_serializer
from django.utils.text import format_lazy
from rest_framework.serializers import ValidationError
from iast.serializers.hook_strategy import HOOK_TYPE_CHOICE
from rest_framework import viewsets
from django.db import connection
logger = logging.getLogger('dongtai-webapi')
from django.db import models
from dongtai.models.strategy import IastStrategyModel
from dongtai.models.user import User
import time
from django.db.models import Q
from dongtai.models.sensitive_info import IastPatternType,IastSensitiveInfoRule
import jq
import re
from dongtai.permissions import TalentAdminPermission

class SensitiveInfoRuleSerializer(serializers.ModelSerializer):
    strategy_name = serializers.SerializerMethodField()
    strategy_id = serializers.SerializerMethodField()
    pattern_type_id = serializers.SerializerMethodField()
    pattern_type_name = serializers.SerializerMethodField()
    class Meta:
        model = IastSensitiveInfoRule
        fields = ['id', 'strategy_name','strategy_id','pattern_type_id','pattern_type_name','pattern','status','latest_time']
    
    def get_strategy_name(self,obj):
        return obj.strategy.vul_name

    def get_strategy_id(self,obj):
        return obj.strategy.id
    
    def get_pattern_type_id(self,obj):
        return obj.pattern_type.id
    def get_pattern_type_name(self,obj):
        return obj.pattern_type.name
class SensitiveInfoPatternTypeSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    class Meta:
        model = IastPatternType
        fields = ['id', 'name', 'url']

    def get_url(self,obj):
        url_dict = {1:'regex',2:'json'} 
        return url_dict.get(obj.id,'')
    

class SensitiveInfoRuleCreateSerializer(serializers.Serializer):
    strategy_id = serializers.IntegerField(required=True)
    pattern_type_id = serializers.IntegerField(required=True)
    pattern = serializers.CharField(required=True)
    status = serializers.IntegerField(required=True)

class _SensitiveInfoArgsSerializer(serializers.Serializer):
    page_size = serializers.IntegerField(default=20,
                                         help_text=_('Number per page'))
    page = serializers.IntegerField(default=1, help_text=_('Page index'))
    name = serializers.CharField(
        default=None,
        required=False,
        help_text=_(
            "The name of the item to be searched, supports fuzzy search."))

class _RegexPatternValidationSerializer(serializers.Serializer):
    pattern = serializers.CharField(help_text=_('regex pattern'))
    test_data = serializers.CharField(help_text=_('the data for test regex'))
  
class SensitiveInfoRuleViewSet(UserEndPoint,viewsets.ViewSet):
    
    permission_classes_by_action = {'create':(TalentAdminPermission,),
                                'update':(TalentAdminPermission,),
                                'destory':(TalentAdminPermission,),}

    def get_permissions(self):
      try:
        return [permission() for permission in self.permission_classes_by_action[self.action]]
      except KeyError:
        return [permission() for permission in self.permission_classes]

    @extend_schema_with_envcheck(
        [_SensitiveInfoArgsSerializer],
        tags=[_('SensitiveInfoRule')],
        summary=_('SensitiveInfoRule List'),
        description=
        _("Get the item corresponding to the user, support fuzzy search based on name."
          ),
    )
    def list(self,request): 
        ser = _SensitiveInfoArgsSerializer(data=request.data)
        try:
            if ser.is_valid(True):
                name = ser.validated_data['name']
                page = ser.validated_data['page']
                page_size = ser.validated_data['page_size']
        except ValidationError as e:
            return R.failure(data=e.detail)
        users = self.get_auth_users(request.user)
        q = Q(user__in=users)
        if name:
            strategys = IastStrategyModel.objects.filter(name__icontains=name).all()
            q = Q(strategy=strategys) & q
        queryset = IastSensitiveInfoRule.objects.filter(q).order_by('-latest_time')
        if name:
            queryset = queryset.filter(name__icontains=name)
        page_summary, page_data = self.get_paginator(queryset, page, page_size)
        return R.success(data=SensitiveInfoRuleSerializer(page_data,many=True).data,page=page_summary)
    
    @extend_schema_with_envcheck(
            request=SensitiveInfoRuleCreateSerializer,
        tags=[_('SensitiveInfoRule')],
        summary=_('SensitiveInfoRule Create'),
        description=
        _("Get the item corresponding to the user, support fuzzy search based on name."
          ),
    )
    def create(self,request):
        ser = SensitiveInfoRuleCreateSerializer(data=request.data)
        try:
            if ser.is_valid(True):
                strategy_id = ser.validated_data['strategy_id']
                pattern_type_id = ser.validated_data['pattern_type_id']
                pattern = ser.validated_data['pattern']
                status = ser.validated_data['status']
        except ValidationError as e:
            return R.failure(data=e.detail)
        strategy = IastStrategyModel.objects.filter(pk=strategy_id).first()
        pattern_type = IastPatternType.objects.filter(pk=pattern_type_id).first()
        pattern_test_dict = {1:regexcompile,2:jqcompile}
        test = pattern_test_dict.get(pattern_type_id,None)
        if not test:
            return R.failure()
        status_ = test(pattern)
        if strategy and pattern_type and status_:
            obj = IastSensitiveInfoRule.objects.create(strategy=strategy,
                    pattern_type=pattern_type,
                    pattern=pattern,
                    status=status,
                    user=request.user) 
            return R.success(msg='create success',data=SensitiveInfoRuleSerializer(obj).data)
        else:
            return R.failure()
    @extend_schema_with_envcheck(
        request=SensitiveInfoRuleCreateSerializer,
        tags=[_('SensitiveInfoRule')],
        summary=_('SensitiveInfoRule Update'),
        description=
        _("Get the item corresponding to the user, support fuzzy search based on name."
          ),
    )
    def update(self, request, pk):
        ser = SensitiveInfoRuleCreateSerializer(data=request.data)
        try:
            if ser.is_valid(True):
                strategy_id = ser.validated_data['strategy_id']
                pattern_type_id = ser.validated_data['pattern_type_id']
                pattern = ser.validated_data['pattern']
                status = ser.validated_data['status']
        except ValidationError as e:
            return R.failure(data=e.detail)
        obj = IastSensitiveInfoRule.objects.filter(pk=pk).update(**ser.validated_data,latest_time=time.time())
        return R.success(msg='update success')
    @extend_schema_with_envcheck(
        tags=[_('SensitiveInfoRule')],
        summary=_('SensitiveInfoRule delete'),
        description=
        _("Get the item corresponding to the user, support fuzzy search based on name."
          ),
    )
    def destory(self, request, pk):
        IastSensitiveInfoRule.objects.filter(pk=pk).update(status=-1)
        return R.success(msg='delete success')

    @extend_schema_with_envcheck(
        tags=[_('SensitiveInfoRule')],
        summary=_('SensitiveInfoRule get'),
        description=
        _("Get the item corresponding to the user, support fuzzy search based on name."
          ),
    )
    def retrieve(self, request, pk):
        obj = IastSensitiveInfoRule.objects.filter(pk=pk).first()
        return R.success(data=SensitiveInfoRuleSerializer(obj).data)
class SensitiveInfoPatternTypeView(UserEndPoint):

    @extend_schema_with_envcheck(
        tags=[_('SensitiveInfoRule')],
        summary=_('SensitiveInfoRule Pattern Type List'),
        description=
        _("Get the item corresponding to the user."
          ),
    )
    def get(self,request):
        objs = IastPatternType.objects.all()
        return R.success(data=SensitiveInfoPatternTypeSerializer(objs,many=True).data)


class SensitiveInfoPatternValidationView(UserEndPoint):
    @extend_schema_with_envcheck(
        request=_RegexPatternValidationSerializer,
        tags=[_('SensitiveInfoRule')],
        summary=_('SensitiveInfoRule validated_data'),
        description=
        _("Get the item corresponding to the user, support fuzzy search based on name."
          ),
    )
    def post(self,request,pattern_type):
        pattern_test_dict = {'regex':regextest,'json':jsontest}
        ser = _RegexPatternValidationSerializer(data=request.data)
        try:
            if ser.is_valid(True):
                test_data = ser.validated_data['test_data']
                pattern = ser.validated_data['pattern']
            if pattern_type not in pattern_test_dict.keys():
                return R.failure()
        except ValidationError as e:
            return R.failure(data=e.detail)
        test = pattern_test_dict[pattern_type]
        data, status = test(test_data,pattern)
        return R.success(data={'status':status,'data':data})
def regexcompile(pattern):
    try:
        regex = re.compile(pattern)
    except Exception as e:
        print(e)
        return False
    return True

def jqcompile(pattern):
    try:
        regex = jq.compile(pattern)
    except Exception as e:
        print(e)
        return False
    return True

def regextest(test_data,pattern):
    try:
        regex = re.compile(pattern)
    except Exception as e:
        print(e)
        data = ''
        status = 0
        return data,status 
    ret = regex.findall(test_data)
    data = ret[0] if ret else ['']
    return data,1
def jsontest(test_data,pattern):
    try:
        data = jq.compile(pattern).input(text=test_data).text()
        status = 1
    except Exception as e:
        print(e)
        data = ''
        status = 0
    return data, status 
