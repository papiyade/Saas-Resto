from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.test import RequestFactory, TestCase

from apps.restaurants.middleware import RestaurantAccessMiddleware
from apps.restaurants.models import Restaurant


class RestaurantModelTests(TestCase):
    def test_suspend_and_activate(self):
        restaurant = Restaurant.objects.create(name='R1', slug='r1')
        restaurant.suspend()
        restaurant.refresh_from_db()
        self.assertFalse(restaurant.is_active)
        self.assertEqual(restaurant.status, Restaurant.Status.SUSPENDED)

        restaurant.activate()
        restaurant.refresh_from_db()
        self.assertTrue(restaurant.is_active)
        self.assertEqual(restaurant.status, Restaurant.Status.ACTIVE)


class RestaurantAccessMiddlewareTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.restaurant = Restaurant.objects.create(name='R2', slug='r2', is_active=False)
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username='staff',
            password='pass1234',
            restaurant=self.restaurant,
            is_platform_admin=False,
        )

    def test_blocks_suspended_restaurant(self):
        request = self.factory.get('/api/v1/restaurant/orders/')
        request.user = self.user

        middleware = RestaurantAccessMiddleware(lambda req: HttpResponse('ok'))
        response = middleware(request)

        self.assertEqual(response.status_code, 423)
