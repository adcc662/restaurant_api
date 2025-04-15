from django.contrib import admin
from .models import Restaurant, Review

# Register your models here.

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'url', 'rating')
    search_fields = ('name', 'slug')
    readonly_fields = ('slug', 'rating')
    list_filter = ('rating',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'rating', 'created')
    search_fields = ('name', 'restaurant__name', 'description')
    readonly_fields = ('slug', 'created')
    list_filter = ('rating', 'created', 'restaurant')
    date_hierarchy = 'created'
