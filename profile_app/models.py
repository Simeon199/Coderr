from django.db import models
from django.conf import settings

class CustomerProfile(models.Model):
    """Lightweight profile for customers - links to CustomUser"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='customer_profile'
    )
    # username = models.CharField(max_length=100, blank=True)
    # first_name = models.CharField(max_length=100, blank=True)
    # last_name = models.CharField(max_length=100, blank=True)
    # file = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.user.username}"

# PROPOSED CHANGE (commented):
# Move common profile fields into `CustomUser` and keep only the
# relation plus business-specific fields here. Uncomment and run
# a data migration to copy data from old profile fields into
# `CustomUser` before removing duplicated fields.
#
# class CustomerProfile(models.Model):
#     """Lightweight profile for customers - links to CustomUser"""
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='customer_profile'
#     )
#
#     def __str__(self):
#         return f"{self.user.username}"
#
# class BusinessProfile(models.Model):
#     """Business-specific profile with additional fields"""
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='business_profile'     
#     )
#
#     # Business-specific fields only
#     location = models.CharField(max_length=100, blank=True)
#     tel = models.CharField(max_length=20, blank=True)
#     description = models.TextField(blank=True)
#     working_hours = models.CharField(max_length=50, blank=True)
#
#     def __str__(self):
#         return f"{self.user.username}"

class BusinessProfile(models.Model):
    """Business-specific profile with additional fields"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='business_profile'     
    )
    
    # username = models.CharField(max_length=100, blank=True)
    # first_name = models.CharField(max_length=100, blank=True)
    # last_name = models.CharField(max_length=100, blank=True)

    # Business-specific fields only

    location = models.CharField(max_length=100, blank=True)
    tel = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    working_hours = models.CharField(max_length=50, blank=True)

    # file = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.user.username}" 