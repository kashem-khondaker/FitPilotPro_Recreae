from django.db import models
from accounts.models import CustomUser
from classes.models import FitnessClass 
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Feedback(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='feedbacks')
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE, related_name='feedbacks')
    rating = models.IntegerField( validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField( max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.fitness_class.name} - {self.rating}"