from typing import Union
from collections.abc import Iterable
from dongtai.models.strategy import IastStrategyModel
from dongtai.models.vulnerablity import IastVulnerabilityModel
from dongtai.models.hook_type import HookType
from django.db.models import Q
from dongtai.models.vul_level import IastVulLevel
import time

def weeks_ago(week: int = 1):

    weekend = 7 * week
    current_timestamp = int(time.time())
    weekend_ago_time = time.localtime(current_timestamp - 86400 * weekend)
    weekend_ago_time_str = str(weekend_ago_time.tm_year) + "-" + str(weekend_ago_time.tm_mon) + "-" + str(
        weekend_ago_time.tm_mday) + " 00:00:00"
    beginArray = time.strptime(weekend_ago_time_str, "%Y-%m-%d %H:%M:%S")

    beginT = int(time.mktime(beginArray))
    return current_timestamp, beginT, weekend

def get_summary_by_agent_ids(agent_ids: Iterable):
    data = {}
    data['type_summary'] = []
    data['day_num'] = []
    data['level_count'] = []
    queryset = IastVulnerabilityModel.objects.filter(
        agent_id__in=agent_ids).values("hook_type_id", 'strategy_id',
                                       "level_id", "latest_time")
    q = ~Q(hook_type_id=0)
    queryset = queryset.filter(q)
    typeArr = {}
    typeLevel = {}
    levelCount = {}
    strategy_ids = queryset.values_list('strategy_id',
                                        flat=True).distinct()
    strategys = {
        strategy['id']: strategy
        for strategy in IastStrategyModel.objects.filter(
            pk__in=strategy_ids).values('id', 'vul_name').all()
    }
    hook_type_ids = queryset.values_list('hook_type_id',
                                         flat=True).distinct()
    hooktypes = {
        hooktype['id']: hooktype
        for hooktype in HookType.objects.filter(
            pk__in=hook_type_ids).values('id', 'name').all()
    }
    if queryset:
        for one in queryset:
            hook_type = hooktypes.get(one['hook_type_id'], None)
            hook_type_name = hook_type['name'] if hook_type else None
            strategy = strategys.get(one['strategy_id'], None)
            strategy_name = strategy['vul_name'] if strategy else None
            type_ = list(
                filter(lambda x: x is not None,
                       [strategy_name, hook_type_name]))
            one['type'] = type_[0] if type_ else ''
            typeArr[one['type']] = typeArr.get(one['type'], 0) + 1
            typeLevel[one['type']] = one['level_id']
            levelCount[one['level_id']] = levelCount.get(
                one['level_id'], 0) + 1
        typeArrKeys = typeArr.keys()
        for item_type in typeArrKeys:
            data['type_summary'].append({
                'type_name': item_type,
                'type_count': typeArr[item_type],
                'type_level': typeLevel[item_type]
            })

    current_timestamp, a_week_ago_timestamp, days = weeks_ago(
        week=1)
    vulInfo = queryset.filter(latest_time__gt=a_week_ago_timestamp,
                              latest_time__lt=current_timestamp).values(
                                  "hook_type_id", "latest_time")

    dayNum = {}
    while days >= 0:
        wDay = time.localtime(current_timestamp - 86400 * days)
        wkey = str(wDay.tm_mon) + "-" + str(wDay.tm_mday)
        dayNum[wkey] = 0
        days = days - 1

    if vulInfo:
        for vul in vulInfo:
            timeArr = time.localtime(vul['latest_time'])
            timeKey = str(timeArr.tm_mon) + "-" + str(timeArr.tm_mday)
            dayNum[timeKey] = dayNum.get(timeKey, 0) + 1
    levelInfo = IastVulLevel.objects.all()
    levelIdArr = {}
    levelNum = []
    if levelInfo:
        for level_item in levelInfo:
            levelIdArr[level_item.id] = level_item.name_value
            levelNum.append({
                "level_id": level_item.id,
                "level_name": level_item.name_value,
                "num": levelCount.get(level_item.id, 0)
            })
    data['level_count'] = levelNum
    if dayNum:
        for day_label in dayNum.keys():
            data['day_num'].append({
                'day_label': day_label,
                'day_num': dayNum[day_label]
            })
    return data
