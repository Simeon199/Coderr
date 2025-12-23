from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Stores authentication data and user type.
    """
    TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('business', 'Business')
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='customer')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.username} ({self.get_type_display()})"