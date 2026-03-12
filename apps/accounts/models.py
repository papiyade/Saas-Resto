from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_platform_admin = models.BooleanField(default=False)
    restaurant = models.ForeignKey(
        'restaurants.Restaurant',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users',
    )

    def __str__(self) -> str:
        return self.username
