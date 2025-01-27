from django.db import models


class Recipe(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    ingredients = models.JSONField()
    tags = models.JSONField()

    class Meta:
        db_table = "dishes_recipe"
        managed = False

    def __str__(self):
        return self.name
