def parse_target_values_from_vul_stack(vul_stack):
    return [i['targetValues'] for i in vul_stack[0]]
