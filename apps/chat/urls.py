from django.urls import path, include

from .views import *
from .routing import websocket_urlpatterns

urlpatterns = [
    path('', chat_list, name='chat_list'),
    path('<str:recipient_username>/', chat_room, name='chat_room'),
    path('send_message/<str:recipient_username>/', send_message, name='send_message'),
    path('ws/chat/<str:room_name>/', ws_chat, name='ws_chat'),
]