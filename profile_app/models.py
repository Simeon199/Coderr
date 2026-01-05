from django.db import models
from django.conf import settings

class AbstractProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='%(class)s_profile'
    )
    username = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    file = models.CharField(max_length=100, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.username}"

class CustomerProfile(AbstractProfile):
    pass

class BusinessProfile(AbstractProfile):
    location = models.CharField(max_length=100, blank=True)
    tel = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    working_hours = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.location}" 