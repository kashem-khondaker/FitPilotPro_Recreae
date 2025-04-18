from django.db import models
from accounts.models import CustomUser
from memberships.models import MembershipPlan, Membership
import uuid

# Create your models here.

class Payment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='payments')
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE, related_name='payments', null=True, blank=True)
    membership_plan = models.ForeignKey(MembershipPlan, on_delete=models.CASCADE, related_name='payments', null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)  # e.g., 'Credit Card', 'PayPal'
    transaction_id = models.CharField(max_length=64, unique=True)
    is_successful = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = str(uuid.uuid4())  # Generate a unique transaction ID
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.payment_date}"