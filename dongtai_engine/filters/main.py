from urllib.parse import urlparse


def vul_filter(stack, source_sign, sink_sign, taint_value, vul_type):
    if vul_type == 'ssrf':
        try:
            target_url = stack[0][-1]['sourceValues']
            res = urlparse(target_url)
            afterurl = target_url.replace(taint_value, '')
            res_after_replace = urlparse(afterurl)
        except Exception as e:
            return False
        if res.netloc == res_after_replace.netloc:
            return False
        return True
    return True
