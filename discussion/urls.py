from django.urls import path

from discussion import views

urlpatterns = [
    path('', views.DisplayThemesView.as_view(), name='main_page'),
    path('discussion/create/', views.CreateThemeView.as_view(), name='create_theme'),
    path('discussion/description/<int:id>/', views.DescriptionThemeView.as_view(), name='description_theme'),
    path('discussion/<str:theme_id>/', views.DiscussionView.as_view(), name='discussion'),
]
