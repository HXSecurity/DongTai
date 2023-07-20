from urllib.parse import urlparse


def vul_filter(stack, source_sign, sink_sign, taint_value, vul_type):
    if vul_type == "reflected-xss":
        target_signature = stack[0][0]["signature"]
        filter_source_signature = [
            "javax.servlet.http.HttpServletRequest.getHeader(java.lang.String)",
            "javax.servlet.http.HttpServletRequest.getHeaderNames()",
            "javax.servlet.http.HttpServletRequest.getParts()",
            "javax.servlet.http.HttpServletRequest.getPart(java.lang.String)",
            "javax.servlet.http.HttpServletRequest.getHeaders(java.lang.String)",
            "jakarta.servlet.http.HttpServletRequest.getHeader(java.lang.String)",
            "jakarta.servlet.http.HttpServletRequest.getHeaders(java.lang.String)",
            "jakarta.servlet.http.HttpServletRequest.getHeaderNames()",
            "jakarta.servlet.http.HttpServletRequest.getParts()",
            "jakarta.servlet.http.HttpServletRequest.getPart(java.lang.String)",
            "org.apache.struts2.dispatcher.multipart.MultiPartRequest.getParameterValues(java.lang.String)",
            "org.apache.commons.fileupload.FileUploadBase.parseRequest(org.apache.commons.fileupload.RequestContext)",
        ]
        if target_signature in filter_source_signature:
            return False
        return True
    return True
