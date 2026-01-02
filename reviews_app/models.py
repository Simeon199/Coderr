from django.db import models
from profile_app.models import CustomerProfile, BusinessProfile

class Review:
    business_user = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='assigned_business_user', null=True, blank=True)
    reviewer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='assigned_customer_reviewer', null=True, blank=True)
    rating = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return f"{self.rating}"
