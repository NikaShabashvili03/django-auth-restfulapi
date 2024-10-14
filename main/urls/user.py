# urls.py

from django.urls import path
from main.views.user import LoginView, ProfileView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
