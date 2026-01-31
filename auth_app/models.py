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
    # username, email, first_name and last_name are automatically 
    # inherited from the AbstractUser and don't have to be declared manually! 
    
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='customer')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.username}"

# PROPOSED CHANGE (commented):
# Add a common profile field `file` to `CustomUser` and keep
# `first_name`/`last_name` inherited from `AbstractUser`.
# This block is a suggested replacement; leave commented until
# you create the migration and copy data from existing profiles.
#
# class CustomUser(AbstractUser):
#     """
#     Custom user model extending Django's AbstractUser.
#     Stores authentication data and common profile fields.
#     """
#     TYPE_CHOICES = (
#         ('customer', 'Customer'),
#         ('business', 'Business')
#     )
#
#     # Common profile field (moved from profile models)
#     file = models.CharField(max_length=100, null=True, blank=True)
#
#     # user type classification
#     type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='customer')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         verbose_name = 'User'
#         verbose_name_plural = 'Users'
#
#     def __str__(self):
#         return f"{self.username}"