from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DishViewSet, DishRecommendationView

router = DefaultRouter()
router.register(r'dishes', DishViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('recommendations/', DishRecommendationView.as_view(), name='recommendations'),
]