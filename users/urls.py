from django.urls import path
from .views import UserCreateView, UserDetailView, UserUpdateView

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="register"),
    path("update/", UserUpdateView.as_view(), name="update"),
    path("user/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
]
