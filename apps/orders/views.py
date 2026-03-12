from rest_framework import viewsets

from apps.orders.models import Category, MenuItem, Order
from apps.orders.permissions import HasRestaurantScope
from apps.orders.serializers import CategorySerializer, MenuItemSerializer, OrderSerializer


class RestaurantScopedViewSet(viewsets.ModelViewSet):
    permission_classes = [HasRestaurantScope]

    def get_queryset(self):
        return self.queryset.filter(restaurant=self.request.user.restaurant).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(restaurant=self.request.user.restaurant)


class CategoryViewSet(RestaurantScopedViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class MenuItemViewSet(RestaurantScopedViewSet):
    queryset = MenuItem.objects.select_related('category').all()
    serializer_class = MenuItemSerializer


class OrderViewSet(RestaurantScopedViewSet):
    queryset = Order.objects.select_related('created_by').all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        serializer.save(restaurant=self.request.user.restaurant, created_by=self.request.user)
