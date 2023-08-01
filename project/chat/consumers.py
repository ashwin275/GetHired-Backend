import json
import logging

from users.models import Account
from channels.generic.websocket import AsyncWebsocketConsumer  #type:ignore
from channels.db import database_sync_to_async #type:ignore

logger = logging.getLogger(__name__)
class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
    
        logger.debug("WebSocket connected")
        # self.user = self.scope.get("user")
        # print('autheticated-user',self.user)
        room_name = self.scope["url_route"]["kwargs"]["user_id"]
        user_instance = await self.get_user(room_name)
        room_group_name = f"chat_{user_instance.id}"

        # Join room group
        await self.channel_layer.group_add(room_group_name, self.channel_name)
        
        await self.accept()
        logger.debug(f"WebSocket accepted for room: {room_name}")



    async def disconnect(self, close_code):
        logger.debug("WebSocket disconnected")
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)


    @database_sync_to_async
    def get_user(self, user_id):
        return Account.objects.get(id=user_id)
    

    # Receive message from WebSocket
    async def receive(self, text_data):
        logger.debug("WebSocket received a message")
        
        text_data_json = json.loads(text_data)
        event = text_data_json.get("event")
       
        if event == "chat":
            
            message = text_data_json.get("message")
            
            to = text_data_json.get("to")
            frm = text_data_json.get("from")

            user_instance = await self.get_user(to)
            room_group_name = f"chat_{user_instance.id}"
            await self.channel_layer.group_send(
            room_group_name, {
                "type": "chat",
                "message": message,
                
                 'message': {
                            "event": "chatmessage",
                            "content": message,
                            "sender": to,
                            "reciever":frm,
                        }
            }
        )
            
        else :
            pass






        # Send message to room group
        

    # Receive message from room group
    async def chat(self, event):
        logger.debug("Sending message to WebSocket")
        message = event["message"]
        sender = event.get("sender", "Anonymous")

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message,"sender": sender }))
