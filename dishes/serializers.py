from rest_framework import serializers
from .models import Dish, Recipe


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ["id", "name", "image", "cuisine", "date_last_made", "rating", "time_to_make"]


class DishLimitedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ["id"]


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ["id", "name", "tags"]
