from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Shop
from .serializers import ShopSerializer
import json

class ShopConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'create':
            serializer_shops = ShopSerializer(data=data.get('shop'))
            if serializer_shops.is_valid():
                shop = serializer_shops.save()
                await self.send_shop_update(shop)
        elif action == 'update':
            shop_id = data.get('shop_id')
            shop = Shop.objects.get(id=shop_id)
            serializer_shops = ShopSerializer(shop, data=data.get('shop'))
            if serializer_shops.is_valid():
                shop = serializer_shops.save()
                await self.send_shop_update(shop)

    async def send_shop_update(self, shop):
        serializer_shops = ShopSerializer(shop)
        await self.send(json.dumps({
            'action': 'update',
            'shop': serializer_shops.data
        }))



