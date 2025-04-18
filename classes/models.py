from django.db import models
from django.core.exceptions import ValidationError
from accounts.models import CustomUser
from cloudinary.models import CloudinaryField

# Create your models here.

class FitnessClass(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = CloudinaryField('Class_Image', null=True, blank=True)
    duration = models.IntegerField()
    max_capacity = models.IntegerField()
    instructor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='fitness_classes')
    schedule = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def is_fully_booked(self):
        return self.bookings.count() >= self.max_capacity

    def clean(self):
        super().clean()
        if self.max_capacity <= 0:
            raise ValidationError("Max capacity must be a positive integer.")

class ClassBooking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='class_bookings')
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'fitness_class')

    def __str__(self):
        return f"{self.user.username} - {self.fitness_class.name}"

    def clean(self):
        super().clean()
        if self.fitness_class.is_fully_booked():
            raise ValidationError("This class is fully booked.")