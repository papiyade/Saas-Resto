from rest_framework import serializers

from apps.restaurants.models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'slug', 'is_active', 'status', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
