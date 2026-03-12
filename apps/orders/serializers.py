from rest_framework import serializers

from apps.orders.models import Category, MenuItem, Order


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'restaurant', 'name', 'created_at', 'updated_at']
        read_only_fields = ['restaurant', 'created_at', 'updated_at']


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'restaurant', 'category', 'name', 'price', 'is_available', 'created_at', 'updated_at']
        read_only_fields = ['restaurant', 'created_at', 'updated_at']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'restaurant', 'created_by', 'kind', 'status', 'created_at', 'updated_at']
        read_only_fields = ['restaurant', 'created_by', 'created_at', 'updated_at']
