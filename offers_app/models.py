from django.db import models
from auth_app.models import CustomUser

class UserDetails(models.Model):
    user = models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='user_details', 
        null=True, 
        blank=True
    )
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Offer(models.Model):
    user = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='user_offers',
        null=True,
        blank=True
    )
    title = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='offers/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    min_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    min_delivery_time = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title
    
class OfferDetail(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='offer_details_user',
        null=True,
        blank=True
    )
    offer = models.ForeignKey(
        Offer, 
        on_delete=models.CASCADE, 
        related_name='offer_details'
    )
    title = models.CharField(max_length=255, null=True, blank=True)
    revisions = models.IntegerField(null=True, blank=True)
    delivery_time_in_days = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    features = models.JSONField(null=True, blank=True)
    offer_type = models.CharField(max_length=20, choices=[
        ('basic', 'Basic'), 
        ('standard', 'Standard'), 
        ('premium', 'Premium')], 
        null=True, 
        blank=True)

    def __str__(self):
        return self.title