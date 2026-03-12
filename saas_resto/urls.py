from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.accounts.views import LoginView
from apps.orders.views import CategoryViewSet, MenuItemViewSet, OrderViewSet
from apps.restaurants.views import RestaurantViewSet

router = DefaultRouter()
router.register(r'admin/restaurants', RestaurantViewSet, basename='admin-restaurants')
router.register(r'restaurant/categories', CategoryViewSet, basename='restaurant-categories')
router.register(r'restaurant/menu-items', MenuItemViewSet, basename='restaurant-menu-items')
router.register(r'restaurant/orders', OrderViewSet, basename='restaurant-orders')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/login/', LoginView.as_view(), name='login'),
    path('api/v1/', include(router.urls)),
]
