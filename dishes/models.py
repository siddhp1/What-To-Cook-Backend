from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Dish(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="static/dishes/")
    cuisine = models.CharField(max_length=100)
    date_last_made = models.DateField()
    rating = models.IntegerField(validators=[MinValueValidator(2), MaxValueValidator(10)])
    time_to_make = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return self.name


class Recipe(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    ingredients = models.JSONField(null=True, default=list)
    tags = models.JSONField(null=True, default=list)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ingredients"
    )
    name = models.CharField(max_length=100)
    count = models.IntegerField()

    def __str__(self):
        return f"{self.name}: {self.count}"
