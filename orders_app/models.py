from django.db import models
from profile_app.models import CustomerProfile, BusinessProfile

class OrderFeatures(models.Model):
    feature = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.feature}"

class Order(models.Model):
    customer_user = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='assigned_customer_profile', null=True, blank=True)
    business_user = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='assigned_business_profile', null=True, blank=True)
    title = models.CharField()
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.IntegerField()
    features = models.ManyToManyField(OrderFeatures, related_name='orders', blank=True, null=True)
    offer_type = models.CharField()
    status = models.CharField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return f"{self.title}"
