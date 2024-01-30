import logging
from shops_online.settings import LOGGER_NAME

class LogAPIMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = LOGGER_NAME
        
    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        method_name = view_func.__name__
        LOGGER_NAME.info(f"Вызван метод API: {method_name}")
        
        return None






