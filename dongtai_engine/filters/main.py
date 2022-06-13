from urllib.parse import urlparse


def vul_filter(stack, source_sign, sink_sign, taint_value, vul_type, agent_id):
    source_signature = stack[0][0]['signature']
    if (vul_type != 'trust-boundary-violation' and source_signature == 'javax.servlet.http.HttpServletRequest.getSession()'):
        return False
    if vul_type == 'ssrf' or vul_type == 'unvalidated-redirect':
        try:
            target_url = stack[0][-1]['sourceValues']
            res = urlparse(target_url)
            afterurl = target_url.replace(taint_value, '')
            res_after_replace = urlparse(afterurl)
        except Exception as e:
            return False
        if not res.scheme and not res.netloc:
            return True
        if res.netloc == res_after_replace.netloc:
            return False
        return True
    elif vul_type == 'reflected-xss':
        target_signature = stack[0][0]['signature']
        filter_source_signature = [
            'javax.servlet.http.HttpServletRequest.getHeader(java.lang.String)',
            'javax.servlet.http.HttpServletRequest.getHeaderNames()',
            'javax.servlet.http.HttpServletRequest.getParts()',
            'javax.servlet.http.HttpServletRequest.getPart(java.lang.String)',
            'javax.servlet.http.HttpServletRequest.getHeaders(java.lang.String)',
            'jakarta.servlet.http.HttpServletRequest.getHeader(java.lang.String)',
            'jakarta.servlet.http.HttpServletRequest.getHeaders(java.lang.String)',
            'jakarta.servlet.http.HttpServletRequest.getHeaderNames()',
            'jakarta.servlet.http.HttpServletRequest.getParts()',
            'jakarta.servlet.http.HttpServletRequest.getPart(java.lang.String)',
            'org.apache.struts2.dispatcher.multipart.MultiPartRequest.getParameterValues(java.lang.String)',
            'org.apache.commons.fileupload.FileUploadBase.parseRequest(org.apache.commons.fileupload.RequestContext)'
        ]
        if target_signature in filter_source_signature:
            return False
        return True
    elif vul_type == 'reflection-injection':
        target_value = stack[0][-1]['sourceValues']
        if target_value.startswith('sun.net.www.protocol'):
            return False
        return True
    elif vul_type == 'unsafe-json-deserialize':
        if stack[0][-1]['signature'].startswith('com.alibaba.fastjson'):
            from dongtai_common.models.asset import Asset
            asset = Asset.objects.filter(
                agent_id=agent_id,
                package_name__icontains="maven:com.alibaba:fastjson:").values(
                    'version').first()
            if asset:
                from packaging import version
                if version.parse(asset['version']) > version.parse('1.2.80'):
                    return False
        return True
    return True
