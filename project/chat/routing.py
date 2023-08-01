
from django.urls import re_path,path

from . import consumers

websocket_urlpatterns = [
    path("ws/chat/<user_id>/", consumers.ChatConsumer.as_asgi()),
]