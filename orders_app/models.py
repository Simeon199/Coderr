from django.db import models
from profile_app.models import CustomerProfile, BusinessProfile
from offers_app.models import Offer, OfferDetail

class OrderFeatures(models.Model):
    feature = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.feature}"

class Order(models.Model):
    customer_user = models.ForeignKey(
        CustomerProfile, 
        on_delete=models.CASCADE, 
        related_name='assigned_customer_profile', 
        null=True, 
        blank=True
    )
    business_user = models.ForeignKey(
        BusinessProfile, 
        on_delete=models.CASCADE, 
        related_name='assigned_business_profile', 
        null=True, 
        blank=True
    )
    offers = models.ForeignKey(
        Offer, 
        on_delete=models.CASCADE, 
        related_name='orders', 
        blank=True, 
        null=True
    )
    offer_detail = models.ForeignKey(
        OfferDetail,
        on_delete=models.CASCADE,
        related_name='orders',
        blank=True,
        null=True
    )
    title = models.CharField(max_length=255)
    revisions = models.IntegerField(default=0)
    delivery_time_in_days = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    features = models.ManyToManyField(OrderFeatures, related_name='order_features', blank=True)
    offer_type = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default='in_progress')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"