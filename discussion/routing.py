from django.urls import path

from discussion import consumers


websocket_urlpatterns = [
    path('ws/chat/<room_name>/', consumers.ChatConsumer),
]