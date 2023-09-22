import time
from collections.abc import Iterable

from django.db.models import Count, Q, Value
from django.db.models.query import QuerySet

from dongtai_common.models.hook_type import HookType
from dongtai_common.models.strategy import IastStrategyModel
from dongtai_common.models.vul_level import IastVulLevel
from dongtai_common.models.vulnerablity import IastVulnerabilityModel


def weeks_ago(week: int = 1):
    weekend = 7 * week
    current_timestamp = int(time.time())
    weekend_ago_time = time.localtime(current_timestamp - 86400 * weekend)
    weekend_ago_time_str = (
        str(weekend_ago_time.tm_year)
        + "-"
        + str(weekend_ago_time.tm_mon)
        + "-"
        + str(weekend_ago_time.tm_mday)
        + " 00:00:00"
    )
    beginArray = time.strptime(weekend_ago_time_str, "%Y-%m-%d %H:%M:%S")

    beginT = int(time.mktime(beginArray))
    return current_timestamp, beginT, weekend


def get_summary_by_agent_ids(agent_ids: Iterable):
    data = {}
    data["type_summary"] = []
    data["level_count"] = []
    queryset = IastVulnerabilityModel.objects.filter(agent_id__in=agent_ids, is_del=0).values(
        "hook_type_id", "strategy_id", "level_id", "latest_time"
    )
    q = ~Q(hook_type_id=0)
    queryset = queryset.filter(q)
    typeArr = {}
    typeLevel = {}
    levelCount = {}
    strategy_ids = queryset.values_list("strategy_id", flat=True).distinct()
    strategys = {
        strategy["id"]: strategy
        for strategy in IastStrategyModel.objects.filter(pk__in=strategy_ids).values("id", "vul_name").all()
    }
    hook_type_ids = queryset.values_list("hook_type_id", flat=True).distinct()
    hooktypes = {
        hooktype["id"]: hooktype
        for hooktype in HookType.objects.filter(pk__in=hook_type_ids).values("id", "name").all()
    }
    if queryset:
        for one in queryset:
            hook_type = hooktypes.get(one["hook_type_id"], None)
            hook_type_name = hook_type["name"] if hook_type else None
            strategy = strategys.get(one["strategy_id"], None)
            strategy_name = strategy["vul_name"] if strategy else None
            type_ = list(filter(lambda x: x is not None, [strategy_name, hook_type_name]))
            one["type"] = type_[0] if type_ else ""
            typeArr[one["type"]] = typeArr.get(one["type"], 0) + 1
            typeLevel[one["type"]] = one["level_id"]
            levelCount[one["level_id"]] = levelCount.get(one["level_id"], 0) + 1
        typeArrKeys = typeArr.keys()
        data["type_summary"].extend(
            {
                "type_name": item_type,
                "type_count": typeArr[item_type],
                "type_level": typeLevel[item_type],
            }
            for item_type in typeArrKeys
        )

    current_timestamp, a_week_ago_timestamp, days = weeks_ago(week=1)
    daylist = []
    while days >= 0:
        wtimestamp = current_timestamp - 86400 * days
        wDay = time.localtime(wtimestamp)
        wkey = str(wDay.tm_mon) + "-" + str(wDay.tm_mday)
        daylist.append([wtimestamp, wkey])
        days = days - 1
    timestamp_gt = current_timestamp
    queryset_list = []
    queryset_ = IastVulnerabilityModel.objects.filter(agent_id__in=agent_ids, is_del=0)
    for timestamp, _ in daylist:
        queryset_list.append(geneatre_vul_timerange_count_queryset(queryset_, timestamp_gt, timestamp, wkey))
        timestamp_gt = timestamp
    if len(queryset_list) > 1:
        start_query_set = queryset_list[0]
        final_query_set = start_query_set.union(*queryset_list[1:], all=True)
    day_num_dict = {}
    for i in final_query_set:
        if i["day_label"] in day_num_dict:
            day_num_dict[i["day_label"]].append(i)
        else:
            day_num_dict[i["day_label"]] = [i]
    day_num_data = []
    last_timestamp: int = 0
    for day_label_i in range(len(daylist)):
        timestamp, day_label = daylist[day_label_i]
        if day_label in day_num_dict:
            # show this day if this day has data
            last_timestamp = timestamp
            obj = get_empty_day_num_num(day_label)
            count = 0
            for i in day_num_dict[day_label]:
                obj["day_num_level_" + str(i["level_id"])] = i["count"]
                count += i["count"]
            obj["day_num"] = count
            day_num_data.append(obj)
        elif day_label_i + 1 < len(daylist) and daylist[day_label_i + 1][1] in day_num_dict:
            # show this day if this yesterday has data
            last_timestamp = timestamp
            day_num_data.append(get_empty_day_num_num(day_label))
    for i in range(1, 8 - len(day_num_data) + 1):
        day = time.localtime(last_timestamp + 86400 * i)
        day_num_data.append(get_empty_day_num_num(str(day.tm_mon) + "-" + str(day.tm_mday)))
    data["day_num"] = day_num_data
    levelInfo = IastVulLevel.objects.all()
    levelIdArr = {}
    levelNum = []
    if levelInfo:
        for level_item in levelInfo:
            levelIdArr[level_item.id] = level_item.name_value
            levelNum.append(
                {
                    "level_id": level_item.id,
                    "level_name": level_item.name_value,
                    "num": levelCount.get(level_item.id, 0),
                }
            )
    data["level_count"] = levelNum
    return data


def get_summary_by_project(project_id: int, project_version_id: int):
    data = {}
    data["type_summary"] = []
    data["level_count"] = []
    queryset = IastVulnerabilityModel.objects.filter(
        project_id=project_id, project_version_id=project_version_id, is_del=0
    ).values("hook_type_id", "strategy_id", "level_id", "latest_time")
    q = ~Q(hook_type_id=0)
    queryset = queryset.filter(q)
    typeArr = {}
    typeLevel = {}
    levelCount = {}
    strategy_ids = queryset.values_list("strategy_id", flat=True).distinct()
    strategys = {
        strategy["id"]: strategy
        for strategy in IastStrategyModel.objects.filter(pk__in=strategy_ids).values("id", "vul_name").all()
    }
    hook_type_ids = queryset.values_list("hook_type_id", flat=True).distinct()
    hooktypes = {
        hooktype["id"]: hooktype
        for hooktype in HookType.objects.filter(pk__in=hook_type_ids).values("id", "name").all()
    }
    if queryset:
        for one in queryset:
            hook_type = hooktypes.get(one["hook_type_id"], None)
            hook_type_name = hook_type["name"] if hook_type else None
            strategy = strategys.get(one["strategy_id"], None)
            strategy_name = strategy["vul_name"] if strategy else None
            type_ = list(filter(lambda x: x is not None, [strategy_name, hook_type_name]))
            one["type"] = type_[0] if type_ else ""
            typeArr[one["type"]] = typeArr.get(one["type"], 0) + 1
            typeLevel[one["type"]] = one["level_id"]
            levelCount[one["level_id"]] = levelCount.get(one["level_id"], 0) + 1
        typeArrKeys = typeArr.keys()
        data["type_summary"].extend(
            {
                "type_name": item_type,
                "type_count": typeArr[item_type],
                "type_level": typeLevel[item_type],
            }
            for item_type in typeArrKeys
        )
    type_summary_total_count = sum(i["type_count"] for i in data["type_summary"])
    for type_summary in data["type_summary"]:
        type_summary["type_total_percentage"] = type_summary["type_total_percentage"] / type_summary_total_count
    current_timestamp, a_week_ago_timestamp, days = weeks_ago(week=1)
    daylist = []
    while days >= 0:
        wtimestamp = current_timestamp - 86400 * days
        wDay = time.localtime(wtimestamp)
        wkey = str(wDay.tm_mon) + "-" + str(wDay.tm_mday)
        daylist.append([wtimestamp, wkey])
        days = days - 1
    timestamp_gt = current_timestamp
    queryset_list = []
    queryset_ = IastVulnerabilityModel.objects.filter(
        project_id=project_id,
        project_version_id=project_version_id,
        is_del=0,
        level_id__in=(1, 2, 3, 5),
    )
    for timestamp, _ in daylist:
        queryset_list.append(geneatre_vul_timerange_count_queryset(queryset_, timestamp_gt, timestamp, wkey))
        timestamp_gt = timestamp
    if len(queryset_list) > 1:
        start_query_set = queryset_list[0]
        final_query_set = start_query_set.union(*queryset_list[1:], all=True)
    day_num_dict = {}
    for i in final_query_set:
        if i["day_label"] in day_num_dict:
            day_num_dict[i["day_label"]].append(i)
        else:
            day_num_dict[i["day_label"]] = [i]
    day_num_data = []
    last_timestamp: int = 0
    for day_label_i in range(len(daylist)):
        timestamp, day_label = daylist[day_label_i]
        if day_label in day_num_dict:
            # show this day if this day has data
            last_timestamp = timestamp
            obj = get_empty_day_num_num(day_label)
            count = 0
            for i in day_num_dict[day_label]:
                obj["day_num_level_" + str(i["level_id"])] = i["count"]
                count += i["count"]
            obj["day_num"] = count
            day_num_data.append(obj)
        elif day_label_i + 1 < len(daylist) and daylist[day_label_i + 1][1] in day_num_dict:
            # show this day if this yesterday has data
            last_timestamp = timestamp
            day_num_data.append(get_empty_day_num_num(day_label))
    for i in range(1, 8 - len(day_num_data) + 1):
        day = time.localtime(last_timestamp + 86400 * i)
        day_num_data.append(get_empty_day_num_num(str(day.tm_mon) + "-" + str(day.tm_mday)))
    data["day_num"] = day_num_data
    levelInfo = IastVulLevel.objects.filter(pk__in=(1, 2, 3, 5)).all()
    levelIdArr = {}
    levelNum = []
    if levelInfo:
        for level_item in levelInfo:
            levelIdArr[level_item.id] = level_item.name_value
            levelNum.append(
                {
                    "level_id": level_item.id,
                    "level_name": level_item.name_value,
                    "num": levelCount.get(level_item.id, 0),
                }
            )
    data["level_count"] = levelNum
    level_total_count = sum(i["num"] for i in data["level_count"])
    for level in data["level_count"]:
        level["level_total_percentage"] = level["num"] / level_total_count
    return data


def get_empty_day_num_num(day_label: str):
    obj = {"day_label": day_label, "day_num": 0}
    for i in (1, 2, 3, 5):
        obj["day_num_level_" + str(i)] = 0
    return obj


def geneatre_vul_timerange_count_queryset(
    vul_queryset: QuerySet,
    time_gt: int,
    time_lt: int,
    day_label: str,
):
    return (
        vul_queryset.filter(latest_time__gt=time_gt, latest_time__lt=time_lt)
        .values("level_id")
        .annotate(count=Count("level_id"), day_label=Value(day_label))
        .order_by("level_id")
        .all()
    )
