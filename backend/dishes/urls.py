from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DishViewSet, QuickDishesView, FavoriteDishesView, OldestDishesView

router = DefaultRouter()
router.register(r'dishes', DishViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('quick/', QuickDishesView.as_view(), name='quick-dishes'),
    path('favorite/', FavoriteDishesView.as_view(), name='favourite-dishes'),
    path('oldest/', OldestDishesView.as_view(), name='oldest-dishes'),
]