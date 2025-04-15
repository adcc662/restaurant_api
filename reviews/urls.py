from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RestaurantViewSet, ReviewViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'restaurant', RestaurantViewSet)
router.register(r'review', ReviewViewSet)

# The API URLs are determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]
