from django.urls import re_path
from shop import consumers

import json

from django.urls import re_path

from .consumers import ShopConsumer

websocket_urlpatterns = [
    re_path(r'ws/shop/$', ShopConsumer.as_asgi()),
]