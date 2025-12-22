from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('business', 'Business'),
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='customer')

    # Add these to resolve the reverse accessor clashes
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='auth_app_user_set',  # Custom related_name
        related_query_name='auth_app_user',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='auth_app_user_permissions_set',  # Custom related_name
        related_query_name='auth_app_user_permission',
    )
    
    def __str__(self):
        return f"{self.username} ({self.get_type_display()})"