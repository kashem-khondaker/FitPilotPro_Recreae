from django.db import models
from accounts.models import CustomUser
from classes.models import FitnessClass , ClassBooking

# Create your models here.

class Attendance(models.Model):
    ATTENDANCE_STATUS = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='attendances')
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE, related_name='attendances')
    class_booking = models.ForeignKey(ClassBooking, on_delete=models.CASCADE, related_name='attendances')
    attendance_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=ATTENDANCE_STATUS, default='absent')

    class Meta:
        unique_together = ('user', 'fitness_class', 'attendance_date')

    def __str__(self):
        return f"{self.user.username} - {self.fitness_class.name} - {self.attendance_date}"