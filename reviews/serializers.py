from rest_framework import serializers
from .models import Restaurant, Review


class RestaurantSerializer(serializers.ModelSerializer):
    """
    Serializer for Restaurant model with validations for required fields
    """
    class Meta:
        model = Restaurant
        fields = ['slug', 'name', 'url', 'image', 'rating']
        read_only_fields = ['slug', 'rating']
        extra_kwargs = {
            'name': {'required': True, 'max_length': 128},
            'image': {'required': True},
        }


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for Review model with validations for required fields
    """
    restaurant_slug = serializers.SlugRelatedField(
        source='restaurant',
        slug_field='slug',
        queryset=Restaurant.objects.all(),
        write_only=True
    )
    
    class Meta:
        model = Review
        fields = ['slug', 'restaurant', 'restaurant_slug', 'name', 'description', 'rating', 'created']
        read_only_fields = ['slug', 'created', 'restaurant']
        extra_kwargs = {
            'name': {'required': True, 'max_length': 128},
            'description': {'required': True},
            'rating': {'required': True, 'min_value': 1, 'max_value': 5},
        }
    
    def validate_rating(self, value):
        """
        Validate that the rating is between 0 and 5
        """
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value
