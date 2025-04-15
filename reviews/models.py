from django.db import models
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator, URLValidator
from slugify import slugify
import uuid

# Create your models here.

class Restaurant(models.Model):
    """
    Restaurant model with name, url, image, and automatically calculated rating
    """
    slug = models.SlugField(max_length=255, unique=True, editable=False)
    name = models.CharField(max_length=128)
    url = models.URLField(max_length=256, blank=True, null=True, validators=[URLValidator()])
    image = models.URLField(validators=[URLValidator()])
    rating = models.FloatField(null=True, blank=True, editable=False)
    
    def save(self, *args, **kwargs):
        # Generate slug if not present
        if not self.slug:
            base_slug = slugify(self.name)
            unique_id = str(uuid.uuid4())[:8]
            self.slug = f"{base_slug}-{unique_id}"
        
        # Calculate average rating
        if not self.pk:  # Skip on new restaurant creation
            super().save(*args, **kwargs)
        else:
            avg_rating = self.reviews.aggregate(Avg('rating'))['rating__avg']
            self.rating = avg_rating
            super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Review(models.Model):
    """
    Review model with a relation to Restaurant and rating between 0-5
    """
    slug = models.SlugField(max_length=255, unique=True, editable=False)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=128)
    description = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    created = models.DateTimeField(auto_now_add=True, editable=False)
    
    def save(self, *args, **kwargs):
        # Generate slug if not present
        if not self.slug:
            base_slug = slugify(self.name)
            unique_id = str(uuid.uuid4())[:8]
            self.slug = f"{base_slug}-{unique_id}"
        
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Update restaurant's average rating
        self.restaurant.save()
    
    def __str__(self):
        return f"{self.name} - {self.restaurant.name} ({self.rating}/5)"
