from django.contrib import admin

from apps.restaurants.models import Restaurant


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'status', 'is_active', 'created_at')
    list_filter = ('status', 'is_active')
    search_fields = ('name', 'slug')
