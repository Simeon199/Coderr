from django.db import models
from django.conf import settings
# from django.contrib.auth.models import User

class AbstractProfile(models.Model):
    # username = models.CharField(max_length=100)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='%(class)s_profile'
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    file = models.CharField(max_length=100, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.user.username}'s {self.__class__.__name__}"

class CustomerProfile(AbstractProfile):
    pass
    # user = models.ForeignKey(
    #     User, 
    #     on_delete=models.CASCADE, related_name="customer_user", 
    #     blank=True, 
    #     null=True
    # )
    # uploaded_at = models.DateTimeField()
    # type = models.CharField(max_length=100)

class BusinessProfile(AbstractProfile):
    # user = models.ForeignKey(
    #     User, 
    #     on_delete=models.CASCADE, related_name="business_user", 
    #     blank=True, 
    #     null=True
    # )
    location = models.CharField(max_length=100)
    tel = models.CharField(max_length=20)
    description = models.TextField()
    working_hours = models.CharField(max_length=50)
    # type = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.username} - {self.location}" 