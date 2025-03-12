"""
Admin Configuration for Car Dealership Application

This module configures the admin interface for the car dealership application.
It registers the CarMake and CarModel models with the admin site.
"""

from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.
admin.site.register(CarMake)
admin.site.register(CarModel)
