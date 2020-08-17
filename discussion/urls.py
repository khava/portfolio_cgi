from django.urls import path

from discussion import views

urlpatterns = [
    path('', views.DisplayTopicsView.as_view(), name='main'),
    path('create_topic/', views.CreateTopicView.as_view(), name='create_topic'),
    path('discussion/<str:room_name>/', views.DiscussionView.as_view(), name='discussion'),
]