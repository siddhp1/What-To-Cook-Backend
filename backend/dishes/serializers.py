from rest_framework import serializers
from .models import Dish

class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ['id', 'name', 'image', 'cuisine', 'date_last_made', 'rating', 'time_to_make']

class DishLimitedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ['id']