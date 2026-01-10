from django.db import models
from profile_app.models import CustomerProfile, BusinessProfile

class Review(models.Model):
    business_user = models.ForeignKey(
        BusinessProfile, 
        on_delete=models.CASCADE, 
        related_name='assigned_business_user', 
        null=True, 
        blank=True
    )
    reviewer = models.ForeignKey(
        CustomerProfile, 
        on_delete=models.CASCADE, 
        related_name='assigned_customer_reviewer', 
        null=True, 
        blank=True
    )
    rating = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.rating}"
