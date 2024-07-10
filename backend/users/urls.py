from django.urls import path
from .views import UserCreateView, UserDetailView

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]