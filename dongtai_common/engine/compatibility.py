def method_pool_is_3(dic: dict) -> bool:
    if 'taintPosition' in dic.keys():
        return True
    return False

KEY_MAPPING = {'O':'objValue','R':'retValue'}

def method_pool_3_to_2(dic: dict) -> dict:
    pdict = {}
    if 'parameterValues' not in dic.keys():
        dic['parameterValues'] = []
    if 'source' not in dic['taintPosition'].keys():
        dic['taintPosition']['source'] = []
    if 'target' not in dic['taintPosition'].keys():
        dic['taintPosition']['target'] = []
    for pv in dic['parameterValues']:
        pdict[pv['index']] = pv['value']
    sourceValues = []
    targetValues = []
    for position in dic['taintPosition']['source']:
        if position == 'O':
            sourceValues.append(dic['objValue'])
        if position == 'R':
            sourceValues.append(dic['retValue'])
        if position.startswith('P'):
            try:
                sourceValues.append(pdict[position])
            except KeyError:
                sourceValues.append('')
    dic['sourceValues'] = ','.join(sourceValues)
    for position in dic['taintPosition']['target']:
        if position == 'O':
            targetValues.append(dic['objValue'])
        if position == 'R':
            targetValues.append(dic['retValue'])
        if position.startswith('P'):
            try:
                targetValues.append(pdict[position])
            except KeyError:
                sourceValues.append('')
    dic['targetValues'] = ','.join(targetValues)
    return dic

def parse_target_value(target_value: str) -> str:
    if not target_value:
        return target_value
    position = target_value.rfind('*')
    origin_str = target_value[0:position][1:-1]
    return origin_str


def parse_target_value_length(target_value: str) -> int:
    if not target_value:
        return 0
    position = target_value.rfind('*')
    len_of_origin = int(target_value[position+1::])
    return len_of_origin

from typing import List


def highlight_target_value(target_value: str, ranges: List) -> str:
    value = parse_target_value(target_value)
    value_origin_len = parse_target_value_length(target_value)
    if not value:
        return target_value
    if ranges and value and len(value) == value_origin_len:
        ranges = sorted(ranges, key = lambda x: x['start'])
        final_str = []
        for range_ in ranges:
            final_str.append(
                f"<emt>{value[range_['start']:range_['stop']]}</emt>")
        return "".join(final_str)
    return f"<emt>{value}</emt>"
