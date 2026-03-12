from rest_framework.permissions import BasePermission


class HasRestaurantScope(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and not user.is_platform_admin
            and getattr(user, 'restaurant_id', None)
        )
