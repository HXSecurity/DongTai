def method_pool_is_3(dic) -> bool:
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
