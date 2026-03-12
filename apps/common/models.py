from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class RestaurantScopedModel(TimeStampedModel):
    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.CASCADE)

    class Meta:
        abstract = True
