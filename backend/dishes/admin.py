from django.contrib import admin
from .models import Dish

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'image', 'cuisine', 'date_last_made', 'rating', 'time_to_make')
    search_fields = ('name', 'user__email')