from django.urls import path

from discussion import consumers


websocket_urlpatterns = [
    path('ws/room_num_participants/', consumers.NumberParticipantsRoomDisplayConsumer),
    path('ws/discussion/<room_id>/', consumers.DiscussionConsumer),
]