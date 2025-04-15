from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Restaurant, Review
from .serializers import RestaurantSerializer, ReviewSerializer
from rest_framework.pagination import LimitOffsetPagination

# Create your views here.

class RestaurantViewSet(viewsets.ModelViewSet):
    """
    API endpoint for CRUD operations on restaurants
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    lookup_field = 'slug'
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'rating']
    ordering = ['name']

    def get_queryset(self):
        queryset = Restaurant.objects.all()
        return queryset

class ReviewViewSet(viewsets.ModelViewSet):
    """
    API endpoint for CRUD operations on reviews
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'slug'
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['restaurant__slug']
    ordering_fields = ['created', 'rating']
    ordering = ['-created']

    def get_queryset(self):
        queryset = Review.objects.all()
        restaurant_slug = self.request.query_params.get('restaurant__slug', None)
        if restaurant_slug is not None:
            queryset = queryset.filter(restaurant__slug=restaurant_slug)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save()
        # The restaurant rating is automatically updated in the Review.save() method
