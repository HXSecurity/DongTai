class DongTaiAppConfigPatch():
    def ready(self):
        try:
            from plugin import monkey_patch
            monkey_patch(self.name)
        except ImportError as e:
            print(e)
            pass



class CSPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response[
            'Content-Security-Policy'] = "default-src * ; img-src *;media-src *;script-src 'self' cdn.jsdelivr.net 'unsafe-inline'"
        return response
