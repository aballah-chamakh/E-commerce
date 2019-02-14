from channels.consumer import AsyncConsumer
import asyncio
from account.models import ParaProfile
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from Order.models import Order
from Order.serializers import OrderSerializer
from channels.db import database_sync_to_async
import json
class NotificationConsumer(AsyncJsonWebsocketConsumer):
    async def websocket_connect(self,event):


        print(self.scope['user'])
        user  = self.scope['user']
        para = user.paraprofile
        para.channel_name = self.channel_name
        print('connect channel : ',para.channel_name)
        para.save()

        await self.accept()
        # await asyncio.sleep(10)
        # await self.send({
        #      'type':'websocket.send',
        #      'text' :'hey buddy' ,
        # })

    async def websocket_receive(self,event):
        print("recieve : ",event)

    async def websocket_disconnect(self,event):
        print('disconnet : ',event)

    async def notification_message(self,event):
        # order = self.get_order(int(event['text']))
        await self.send_json(content=event['text'])
    @database_sync_to_async
    def get_order(order_id):
        order_obj = Order.objects.get(id=order_id)
        serializer = OrderSideListSerializer(order_obj,many=False)
        print(serialier.data)
        return serializer.data
