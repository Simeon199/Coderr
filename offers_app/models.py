from django.db import models
from auth_app.models import CustomUser

class UserDetails(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='user_details')
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class OfferDetail(models.Model):
    offer = models.ForeignKey('Offer', on_delete=models.CASCADE, related_name='offer_details')
    url = models.CharField(max_length=255)

    def __str__(self):
        return self.url
    
class Offer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='offers')
    title = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='offers/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    min_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    min_delivery_time = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title