# accounts/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.managers import CustomUserManager
import uuid
from cloudinary.models import CloudinaryField
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('MEMBER', 'Member'),
        ('STAFF', 'Staff'),
        ('ADMIN', 'Admin'),
    )
    username = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='MEMBER')
    email = models.EmailField(unique=True, max_length=255)
    email_verified = models.BooleanField(default=False)
    phone = models.PositiveIntegerField(unique=True, null=True, blank=True)
    is_verified = models.BooleanField(default=False, verbose_name=_('Is Verified'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    bio = models.TextField(null=True, blank=True)
    profile_picture = CloudinaryField('Profile_Image', null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"