from django.db import models
from accounts.models import CustomUser
from classes.models import FitnessClass

# Create your models here.

class Report(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reports')
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE, related_name='reports')
    report_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return f"Report by {self.user.email} on {self.report_date}"