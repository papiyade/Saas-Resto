from django.conf import settings
from django.db import models

from apps.common.models import RestaurantScopedModel


class Category(RestaurantScopedModel):
    name = models.CharField(max_length=120)

    class Meta:
        unique_together = ('restaurant', 'name')


class MenuItem(RestaurantScopedModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)


class Order(RestaurantScopedModel):
    class Kind(models.TextChoices):
        DINE_IN = 'dine_in', 'Dine in'
        TAKEAWAY = 'takeaway', 'Takeaway'
        DELIVERY = 'delivery', 'Delivery'

    class Status(models.TextChoices):
        NEW = 'new', 'New'
        PREPARING = 'preparing', 'Preparing'
        READY = 'ready', 'Ready'
        SERVED = 'served', 'Served'
        CLOSED = 'closed', 'Closed'

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    kind = models.CharField(max_length=20, choices=Kind.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)


class OrderItem(RestaurantScopedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)


class Payment(RestaurantScopedModel):
    class Method(models.TextChoices):
        CASH = 'cash', 'Cash'
        CARD = 'card', 'Card'
        MOBILE = 'mobile', 'Mobile'

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    method = models.CharField(max_length=20, choices=Method.choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
