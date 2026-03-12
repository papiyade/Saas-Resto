from django.contrib import admin

from apps.orders.models import Category, MenuItem, Order, OrderItem, Payment

admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
