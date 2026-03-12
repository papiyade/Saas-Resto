from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.restaurants.models import Restaurant
from apps.restaurants.permissions import IsPlatformAdmin
from apps.restaurants.serializers import RestaurantSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all().order_by('-created_at')
    serializer_class = RestaurantSerializer
    permission_classes = [IsPlatformAdmin]

    @action(detail=True, methods=['patch'])
    def suspend(self, request, pk=None):
        restaurant = self.get_object()
        restaurant.suspend()
        return Response(self.get_serializer(restaurant).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def activate(self, request, pk=None):
        restaurant = self.get_object()
        restaurant.activate()
        return Response(self.get_serializer(restaurant).data, status=status.HTTP_200_OK)
