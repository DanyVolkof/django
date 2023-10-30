import logging

class LogAPIMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger(__name__)
        
    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        method_name = view_func.__name__
        self.logger.info(f"Вызван метод API: {method_name}")
        
        return None






