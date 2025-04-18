from django.db.models.signals import post_save
from django.dispatch import receiver
from memberships.models import Membership
from payments.models import Payment
from django.utils import timezone

@receiver(post_save, sender=Payment)
def create_membership_on_payment(sender, instance, created, **kwargs):
    if created and instance.is_successful:
        try:
            start_date = timezone.now()
            end_date = start_date + timezone.timedelta(days=instance.membership_plan.duration_in_days)

            membership = Membership.objects.create(
                user=instance.user,
                plan=instance.membership_plan,
                start_date=start_date,
                end_date=end_date,
                is_active=True
            )

            # Link the created membership to the payment
            instance.membership = membership
            instance.save()
        except Exception as e:
            print(f"Error creating membership: {e}")