from django.db import models
from accounts.models import CustomUser

# Create your models here.

class MembershipPlan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_in_days = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Membership(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE , related_name='memberships')
    plan = models.ForeignKey(MembershipPlan, on_delete=models.CASCADE , related_name='memberships')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"