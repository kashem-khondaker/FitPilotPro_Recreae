from django.contrib import admin
from .models import FitnessClass, ClassBooking

# Register your models here.

admin.site.register(FitnessClass)
admin.site.register(ClassBooking)