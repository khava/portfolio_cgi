from django.urls import path

from moderator import views


urlpatterns = [
    path('', views.ThemesListView.as_view(), name='moderator_page'),
    path('theme/<int:theme_id>/', views.ThemeDetailView.as_view(), name='theme_detail'),
    path('theme/<int:theme_id>/comments/<int:discussion_id>/', views.ThemeDiscussionCommentsView.as_view(), name='theme_comments'),
    
]
