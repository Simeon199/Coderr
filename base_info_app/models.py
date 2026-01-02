from django.db import models

# Links to the related objects are missing for the moment

class BaseInfo(models.Model):
    review_count = models.IntegerField()
    average_rating = models.FloatField()
    business_profile_count = models.IntegerField()
    offer_count = models.IntegerField()