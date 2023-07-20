from math import ceil
from typing import List
import logging

logger = logging.getLogger("dongtai-core")


def method_pool_is_3(dic: dict) -> bool:
    if "taintPosition" in dic.keys():
        return True
    return False


KEY_MAPPING = {"O": "objValue", "R": "retValue"}


def method_pool_3_to_2(dic: dict) -> dict:
    pdict = {}
    if "parameterValues" not in dic.keys():
        dic["parameterValues"] = []
    if "source" not in dic["taintPosition"].keys():
        dic["taintPosition"]["source"] = []
    if "target" not in dic["taintPosition"].keys():
        dic["taintPosition"]["target"] = []
    for pv in dic["parameterValues"]:
        pdict[pv["index"]] = pv["value"]
    sourceValues = []
    targetValues = []
    for position in dic["taintPosition"]["source"]:
        if position == "O":
            sourceValues.append(dic["objValue"])
        if position == "R":
            sourceValues.append(dic["retValue"])
        if position.startswith("P"):
            try:
                sourceValues.append(pdict[position])
            except KeyError:
                pass
    dic["sourceValues"] = ",".join(sourceValues)
    for position in dic["taintPosition"]["target"]:
        if position == "O":
            targetValues.append(dic["objValue"])
        if position == "R":
            targetValues.append(dic["retValue"])
        if position.startswith("P"):
            try:
                targetValues.append(pdict[position])
            except KeyError:
                pass
    dic["targetValues"] = ",".join(targetValues)
    return dic


def parse_target_value(target_value: str) -> str:
    if not target_value:
        return target_value
    position = target_value.rfind("*")
    origin_str = target_value[0:position][1:-1]
    return origin_str


def parse_target_value_length(target_value: str) -> int:
    if not target_value:
        return 0
    position = target_value.rfind("*")
    try:
        len_of_origin = int(target_value[position + 1 : :])
    except ValueError as e:
        return len(target_value)
    return len_of_origin


AGENT_DEFAULT_LENGTH = 1024


def xss_prevent(char: str) -> str:
    if char == "<":
        return "&lt;"
    return char


# temporary fit in cython
# def highlight_target_value(target_value: str, ranges: List) -> str:
def highlight_target_value(target_value: str, ranges: list) -> str:
    value = parse_target_value(target_value)
    value_origin_len = parse_target_value_length(target_value)
    if not value:
        return target_value.replace("<", "&lt;")
    sorted_ranges = sorted(ranges, key=lambda x: x["start"])
    for range_ in sorted_ranges:
        if range_["start"] > value_origin_len or range_["stop"] > value_origin_len:
            return f'<em style="color:red;">{value}</em>'
    if sorted_ranges and value and len(value) == value_origin_len:
        final_str = []
        str_dict = {ind: xss_prevent(str_) for ind, str_ in enumerate(value)}
        for range_ in sorted_ranges:
            str_dict[range_["start"]] = (
                '<em style="color:red;">' + str_dict[range_["start"]]
            )
            str_dict[range_["stop"] - 1] = str_dict[range_["stop"] - 1] + "</em>"
        final_str = list(
            map(lambda x: x[1], sorted(str_dict.items(), key=lambda kv: kv[0]))
        )
        return "".join(final_str)
    if len(value) != AGENT_DEFAULT_LENGTH:
        return f'<em style="color:red;">{value}</em>'
    try:
        if sorted_ranges and value and len(value) < value_origin_len:
            begin_part_length = ceil((AGENT_DEFAULT_LENGTH - 3) / 2)
            end_part_length = int((AGENT_DEFAULT_LENGTH - 3) / 2)
            hidden_red_flag = False
            end_part_start_ind = value_origin_len - end_part_length
            str_dict_begin = {
                ind: xss_prevent(str_)
                for ind, str_ in enumerate(value[:begin_part_length])
            }
            str_dict_end = {
                ind + (value_origin_len - end_part_length) + 3: xss_prevent(str_)
                for ind, str_ in enumerate(value[-end_part_length:])
            }
            str_dict = {}
            str_dict.update(str_dict_begin)
            str_dict.update(str_dict_end)
            str_dict[begin_part_length + 2] = "..."
            for range_ in sorted_ranges:
                if (
                    range_["start"] in str_dict.keys()
                    and (range_["stop"] - 1) in str_dict.keys()
                ):
                    str_dict[range_["start"]] = (
                        '<em style="color:red;">' + str_dict[range_["start"]]
                    )
                    str_dict[range_["stop"] - 1] = (
                        str_dict[range_["stop"] - 1] + "</em>"
                    )

                if (
                    range_["start"] in str_dict.keys()
                    and (range_["stop"] - 1) not in str_dict.keys()
                ):
                    str_dict[range_["start"]] = (
                        '<em style="color:red;">' + str_dict[range_["start"]]
                    )
                    str_dict[begin_part_length] = "</em>" + str_dict[begin_part_length]
                    str_dict[begin_part_length] = "</em>" + str_dict[begin_part_length]
                if (
                    range_["start"] not in str_dict.keys()
                    and (range_["stop"] - 1) in str_dict.keys()
                ):
                    str_dict[value_origin_len - end_part_length] = (
                        '<em style="color:red;">'
                        + str_dict[value_origin_len - end_part_length]
                    )
                    str_dict[range_["stop"] - 1] = (
                        str_dict[range_["stop"] - 1] + "</em>"
                    )
                if (
                    range_["start"] not in str_dict.keys()
                    or (range_["stop"]) not in str_dict.keys()
                ):
                    str_dict[begin_part_length + 2] = (
                        '<em style="color:red;">' + "..." + "</em>"
                    )
            final_str = list(
                map(lambda x: x[1], sorted(str_dict.items(), key=lambda kv: kv[0]))
            )
            return "".join(final_str)
    except KeyError as e:
        logger.warning(e, exc_info=e)
    return f'<em style="color:red;">{value}</em>'
