from rest_framework import serializers
from .models import Dish

class DishSerializer(serializers.ModelSerializer):
    full_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Dish
        fields = ['id', 'name', 'image', 'cuisine', 'date_last_made', 'rating', 'time_to_make', 'full_image_url']

    def get_full_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url)
        return None
    
class DishLimitedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ['id', 'name', 'cuisine']  # Assuming you want to include all fields, adjust as necessary