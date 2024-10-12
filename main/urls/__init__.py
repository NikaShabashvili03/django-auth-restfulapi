from django.urls import path, include

urlpatterns = [
    path('user/', include('main.urls.user')),  # Adjust according to your structure
]