######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : middleware
# @created     : 星期一 2月 14, 2022 15:06:25 CST
#
# @description :
######################################################################


import logging
import time

request_logger = logging.getLogger(__name__)
REQUEST_DICT = {}


class RequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        # Only logging "*/api/*" patterns
        apiurl = str(request.get_full_path()) if "/api/" in str(request.get_full_path()) else ""
        response = self.get_response(request)
        timenow = time.time() - start_time
        api_info = REQUEST_DICT.get(
            apiurl,
            {"max_time": 0, "min_time": 0, "average_time": 0, "request_count": 0},
        )
        api_info["max_time"] = (
            timenow if api_info["max_time"] == 0 or api_info["max_time"] < timenow else api_info["max_time"]
        )
        api_info["min_time"] = (
            timenow if api_info["min_time"] == 0 or api_info["min_time"] > timenow else api_info["min_time"]
        )
        api_info["average_time"] = (api_info["average_time"] * api_info["request_count"] + timenow) / (
            api_info["request_count"] + 1
        )
        api_info["request_count"] += 1
        REQUEST_DICT[apiurl] = api_info
        request_logger.error(msg=f"{apiurl} : {timenow}")
        return response

    def process_exception(self, request, exception):
        try:
            raise exception
        except Exception as e:
            request_logger.exception("Unhandled Exception: ", exc_info=e)
        return exception
