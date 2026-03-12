from django.http import JsonResponse


class RestaurantAccessMiddleware:
    """Bloque les utilisateurs d'un restaurant suspendu."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', None)
        if user and user.is_authenticated and not user.is_platform_admin and user.restaurant:
            if not user.restaurant.is_active:
                return JsonResponse({'detail': 'Restaurant suspended'}, status=423)
            request.restaurant = user.restaurant
        return self.get_response(request)
