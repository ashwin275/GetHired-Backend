import json
import logging
import datetime
from users.models import Account
from channels.generic.websocket import AsyncWebsocketConsumer  # type:ignore
from channels.db import database_sync_to_async  # type:ignore
from asgiref.sync import sync_to_async
from .models import Message
from employers.models import JobPost
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

    # async def disconnect(self, close_code):
    #     logger.debug("WebSocket disconnected")
    #     # Leave room group
    #     await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def add_chat(self, data):

        sender = await self.get_user(data['from'])

        recipient = await self.get_user(data['to'])
        post = await self.get_post(data['postId'])
        content = data['content']

        await sync_to_async(Message.objects.create)(sender=sender, recipient=recipient, content=content,postId = post )

        print('message created')

    @database_sync_to_async
    def get_user(self, user_id):
        return Account.objects.get(id=user_id)
    @database_sync_to_async
    def get_post(self,post_id):
        return JobPost.objects.get(id=post_id)

    # Receive message from WebSocket

    async def receive(self, text_data):
        logger.debug("WebSocket received a message")

        text_data_json = json.loads(text_data)
        event = text_data_json.get("event")

        if event == "chat":

            message = text_data_json.get("message")

            to = text_data_json.get("to")
            frm = text_data_json.get("from")
            postId = text_data_json.get("postID")
            data = {'from': frm, 'to': to, 'content': message,'postId':postId}
            await self.add_chat(data)
            user_instance = await self.get_user(to)
            room_group_name = f"chat_{user_instance.id}"
            await self.channel_layer.group_send(
                room_group_name,    {
                    'type': 'chat',
                    
                    'message': {
                            'event': 'chatmessage',
                            'content': message,
                            'sender':frm,
                            'recipient':to,
                            'postId':postId,
                            'created_at':datetime.datetime.now().isoformat()

                    }
                }
            )

        else:
            print('Only Chat features implemented')
            pass

        # Send message to room group

    # Receive message from room group

    async def chat(self, event):
        logger.debug("Sending message to WebSocket")
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
