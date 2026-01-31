from django.db import models
from django.conf import settings

class CustomerProfile(models.Model):
    """Lightweight profile for customers - links to CustomUser"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='customer_profile'
    )

    def __str__(self):
        return f"{self.user.username}"

class BusinessProfile(models.Model):
    """Business-specific profile with additional fields"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='business_profile'     
    )

    # Business-specific fields only

    location = models.CharField(max_length=100, blank=True)
    tel = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    working_hours = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.user.username}" 