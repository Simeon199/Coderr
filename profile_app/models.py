from django.db import models
from auth_app.models import UserProfile

class AbstractProfile(models.Model):
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    file = models.CharField(max_length=100, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.username}"

class CustomerProfile(AbstractProfile):
    user = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="customer_profile"
    )
    uploaded_at = models.DateTimeField()
    type = models.CharField(max_length=100)

class BusinessProfile(AbstractProfile):
    user = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="business_profile"
    )
    location = models.CharField(max_length=100)
    tel = models.CharField(max_length=20)
    description = models.TextField()
    working_hours = models.CharField(max_length=50)
    type = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.username} - {self.location}" 

# class CustomerProfile(models.Model):
#     user = models.IntegerField()
#     username = models.CharField(max_length=100)
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     file = models.CharField(max_length=100),
#     uploaded_at = models.DateTimeField()
#     type = models.CharField(max_length=100)

#     def __str__(self):
#         return f"{self.username} - {self.type}"

# class BusinessProfile(models.Model):
#     user = models.IntegerField()
#     username = models.CharField(max_length=100)
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     file = models.CharField(max_length=100)
#     location = models.CharField(max_length=100)
#     tel = models.CharField(max_length=20)
#     description = models.TextField()
#     working_hours = models.CharField(max_length=50)
#     type = models.CharField(max_length=50)

#     def __str__(self):
#         return f"{self.username} - {self.location}" 