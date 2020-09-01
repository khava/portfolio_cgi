from django.urls import path, include
from django.contrib.auth import views as auth_views

from accounts import views


urlpatterns = [
    path('signup/', views.signup, name = 'signup'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('', include('django.contrib.auth.urls')),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]