from django.urls import path

from discussion import consumers


websocket_urlpatterns = [
    path('ws/discussion/<theme_id>/', consumers.DiscussionConsumer),
    # path('ws/discussion/<theme_id>/room_users/', consumers.RoomUsersDisplayConsumer),
]